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

def create_client(conn, name):
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid

def create_shipment(conn, client_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO shipments (client_id, date) VALUES (?, ?)",
        (client_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    return cur.lastrowid

def insert_shipment_item(conn, shipment_id, fish_type, weight, price):
    total = weight * price
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO shipment_items
        (shipment_id, fish_type, weight, price_per_kg, total)
        VALUES (?, ?, ?, ?, ?)
    """, (shipment_id, fish_type, weight, price, total))
    conn.commit()

def fetch_client_history(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id as shipment_id,
               s.date,
               si.fish_type,
               si.weight,
               si.price_per_kg,
               si.total
        FROM shipments s
        JOIN shipment_items si ON s.id = si.shipment_id
        WHERE s.client_id = ?
        ORDER BY s.date DESC
    """, (client_id,))

    return cur.fetchall()

def get_client_by_name(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM clients WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def get_or_create_client(conn, name):
    client_id = get_client_by_name(conn, name)

    if client_id:
        return client_id
    else:
        return create_client(conn, name)