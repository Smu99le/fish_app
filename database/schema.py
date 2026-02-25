def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fish_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cust_name TEXT,
            phone INTEGER,
            fish_type TEXT,
            kg REAL,
            price REAL,
            total REAL,
            datetime TEXT
        )
    """)
    conn.commit()
