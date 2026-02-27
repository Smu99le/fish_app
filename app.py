import streamlit as st
import re
import pandas as pd

from database.connections import get_connection
from database.schema import create_tables
from database.repository import (
    get_or_create_client,
    get_client_by_name,
    create_shipment,
    insert_shipment_item,
    fetch_client_history,
    fetch_history
)
from services.fish_service import calculate_total
from services.report_service import summarize_by_client
from services.Export_to_excel import to_excel

# --- Init ---
conn = get_connection()
create_tables(conn)

st.set_page_config(page_title="My Fish App")
st.title("Облік риби по ставку 'Хейлове'")
st.write("Головна сторінка")

# --- Input ---
cust_name = st.text_input("Ім'я клієнта")
phone = st.text_input("Телефон")
phone_pattern = r'^(\+380\d{9}|0\d{9})$'
if phone:
    if not re.match(phone_pattern, phone):
        st.error("Невірний формат телефону. Приклад: +380991234567 або 0991234567")
    else:
        st.success("Номер валідний")

kg = st.number_input("Кількість (кг)", min_value=0.0, step=0.1)
price = st.number_input("Ціна за кг", min_value=0.0, step=0.5)

fish_type = st.selectbox(
    "Тип риби",
    ["Короп", "Карась", "Щука", "Амур", "Товстолоб", "Окунь", "Інше"]  # список варіантів риб
)

if "cart" not in st.session_state:
    st.session_state.cart = []

if st.button("Додати позицію"):
    if kg > 0:
        st.session_state.cart.append({
            "fish_type": fish_type,
            "weight": kg,
            "price": price
        })
        st.success("Позицію додано")

st.subheader("Поточні позиції")
st.write(st.session_state.cart)

if st.button("Зберегти відвантаження"):
    if cust_name and st.session_state.cart:
        client_id = get_or_create_client(conn, cust_name)
        shipment_id = create_shipment(conn, client_id)

        for item in st.session_state.cart:
            insert_shipment_item(
                conn,
                shipment_id,
                item["fish_type"],
                item["weight"],
                item["price"]
            )

        st.success("Відвантаження збережено")
        st.session_state.cart = []

# --- Історія конкретного клієнта ---
st.subheader("Історія клієнта")
search_name = st.text_input("Введіть ім'я клієнта для перегляду", key="search_name")

if st.button("Показати історію клієнта"):
    client_id = get_client_by_name(conn, search_name)
    if client_id:
        history = fetch_client_history(conn, client_id)
        if history:
            df_history = pd.DataFrame(history, columns=[
                "Shipment ID", "Дата", "Вид риби", "Вага (кг)", "Ціна/кг", "Сума"
            ])
            st.dataframe(df_history)
            st.write("### Підсумок")
            st.write("Загальна вага:", df_history["Вага (кг)"].sum())
            st.write("Загальна сума:", df_history["Сума"].sum())
        else:
            st.warning("Історія порожня")
    else:
        st.warning("Клієнта не знайдено")

# --- Вся історія ---
st.subheader("Вся історія відвантажень")
if st.button("Показати всю історію"):
    df_all = fetch_history(conn)
    if df_all.empty:
        st.write("Історія порожня")
    else:
        st.dataframe(df_all)

# if st.button("Зберегти"):
#     if cust_name and kg > 0:
#         total = calculate_total(kg, price)
#         insert_fish(conn, cust_name, phone, fish_type, kg, price, total)
#         st.success("Запис збережено")

# --- History ---
# df = fetch_history(conn)
# df_display = df.rename(columns={
#     "cust_name": "Клієнт",
#     "phone": "Телефон",
#     "fish_type": "Вид риби",
#     "kg": "Кілкість (кг)",
#     "price": "Ціна/кг (грн)",
#     "total": "Сума (грн)",
#     "datetime": "Дата"
# })
# st.subheader("Історія відвантажень")
# st.dataframe(df_display)

# --- Summary ---
# summary = summarize_by_client(df)
# summary_display = summary.rename(columns={
#     "cust_name": "Ім'я клієнта",
#     "phone": "Телефон",
#     "total_kg": "Загальна вага (кг)",
#     "total_amount": "Загальна сума (грн)"
# })
#
# st.subheader("Підсумок по клієнтах")
# st.dataframe(summary_display)
# summary = summarize_by_client(df)

# --- Динамічний експорт Excel ---
st.subheader("Експорт в Excel")
export_choice = st.radio("Що експортувати?", ("Вся історія", "Історія клієнта"))

excel_df = None

if export_choice == "Вся історія":
    df = fetch_history(conn)
    if not df.empty:
        excel_df = df
elif export_choice == "Історія клієнта":
    if search_name:
        client_id = get_client_by_name(conn, search_name)
        if client_id:
            history = fetch_client_history(conn, client_id)
            if history:
                excel_df = pd.DataFrame(history, columns=[
                    "Shipment ID", "Дата", "Вид риби", "Вага (кг)", "Ціна/кг", "Сума"
                ])

if excel_df is not None and not excel_df.empty:
    excel_data = to_excel(excel_df)
    st.download_button(
        label="Скачати в Excel",
        data=excel_data,
        file_name="fish_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
