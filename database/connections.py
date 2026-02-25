import sqlite3

def get_connection(db_path: str = "db.sqlite"):
    return sqlite3.connect(db_path, check_same_thread=False)