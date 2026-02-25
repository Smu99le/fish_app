from datetime import datetime

def insert_fish(conn, cust_name, phone, fish_type, kg, price, total):
    cursor = conn.cursor()
    dt_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO fish_history
        (cust_name, phone, fish_type, kg, price, total, datetime)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (cust_name, phone, fish_type, kg, price, total, dt_now))

    conn.commit()


def fetch_history(conn):
    import pandas as pd
    return pd.read_sql("SELECT * FROM fish_history", conn)


def update_fish(conn, record_id, cust_name, phone, fish_type, kg, price, total):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fish_history
        SET cust_name = ?,
            phone = ?,
             fish_type = ?,
             kg = ?,
             price = ?,
             total = ?
        WHERE id = ?
     """, (cust_name, phone, fish_type, kg, price, total, record_id))
    conn.commit()