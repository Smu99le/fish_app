import streamlit as st
import re

from database.connections import get_connection
from database.schema import create_tables
from database.repository import insert_fish, fetch_history, update_fish
from services.fish_service import calculate_total
from services.report_service import summarize_by_client
from io import BytesIO

# --- Init ---
conn = get_connection()
create_tables(conn)

st.set_page_config(page_title="Fish Pool App")
st.title("Облік риби")
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

if st.button("Зберегти"):
    if cust_name and kg > 0:
        total = calculate_total(kg, price)
        insert_fish(conn, cust_name, phone, fish_type, kg, price, total)
        st.success("Запис збережено")

# --- History ---
df = fetch_history(conn)

df_display = df.rename(columns={
    "cust_name": "Клієнт",
    "phone": "Телефон",
    "fish_type": "Вид риби",
    "kg": "Кілкість (кг)",
    "price": "Ціна/кг (грн)",
    "total": "Сума (грн)",
    "datetime": "Дата"
})
st.subheader("Історія відвантажень")
st.dataframe(df_display)

# --- Summary ---
summary = summarize_by_client(df)

summary_display = summary.rename(columns={
    "cust_name": "Ім'я клієнта",
    "phone": "Телефон",
    "total_kg": "Загальна вага (кг)",
    "total_amount": "Загальна сума (грн)"
})

st.subheader("Підсумок по клієнтах")
st.dataframe(summary_display)

summary = summarize_by_client(df)

# Функція для конвертації в Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data

# Генеруємо Excel
if not df.empty:
    excel_data = to_excel(df)

# Кнопка завантаження
st.download_button(
    label="Скачати Excel",
    data=excel_data,
    file_name="fish_history.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# --- Records Edit ---
# st.subheader("Редагування запису")
# if not df.empty:
#     record_id = st.selectbox("Оберіть запис (ID)", df["id"])
#     record = df[df["id"] == record_id].iloc[0]
#     edit_name = st.text_input("Ім'я", record["cust_name"])
#     edit_phone = st.text_input("Телефон", record["phone"])
#     edit_kg = st.number_input("Кг", value=float(record["kg"]))
#     edit_price = st.number_input("Ціна", value=float(record["price"]))
#     edit_fish = st.selectbox(
#         "Тип риби",
#         ["Короп", "Карась", "Щука", "Амур", "Товстолоб", "Окунь", "Інше"],
#         index=["Короп", "Карась", "Щука", "Амур", "Товстолоб", "Окунь", "Інше"].index(record["fish_type"])
#     )
#
#     if st.button("Оновити запис"):
#         new_total = calculate_total(edit_kg, edit_price)
#         update_fish(conn, record_id, edit_name, edit_phone, edit_fish, edit_kg, edit_price, new_total)
#         st.success("Запис оновлено")
#         st.rerun()