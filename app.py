import sqlite3

def init_db():
    conn = sqlite3.connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            f_name TEXT NOT NULL,
            l_bane TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()