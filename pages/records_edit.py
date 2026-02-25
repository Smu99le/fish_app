import streamlit as st
import pandas as pd
from database.connections import get_connection
from datetime import datetime

st.set_page_config(page_title="Records Edit")
st.title("Records Edit")
st.write("Редагування записів")

# Завантаження даних
def load_records():
    with get_connection() as conn:
        df = pd.read_sql("SELECT * FROM fish_history", conn)
    return df

# Збереження змін
def save_records(df):
    with get_connection() as conn:
        for _, row in df.iterrows():
            conn.execute("""
                UPDATE fish_history
                SET cust_name=?, phone=?, fish_type=?, kg=?, price=?, total=?, datetime=?
                WHERE id=?
            """, (row['cust_name'], row['phone'], row['fish_type'],
                  row['kg'], row['price'], row['datetime'], row['id']))
        conn.commit()

# Streamlit UI
st.set_page_config(page_title="Records Edit")
st.title("Records Edit")

df = load_records()

# Data editor
edited_df = st.data_editor(df, num_rows="dynamic")  # або use st.experimental_data_editor(df)

if st.button("Save Changes"):
    save_records(edited_df)
    st.success("Records updated!")