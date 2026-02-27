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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER NOT NULL,
        fish_type TEXT NOT NULL,
        weight REAL NOT NULL,
        price_per_kg REAL NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (shipment_id) REFERENCES shipments(id)
    )
    """)

    conn.commit()