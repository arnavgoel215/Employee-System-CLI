import sqlite3

def init_db():
    conn = sqlite3.connect("employee_system.db")
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paychecks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            hours INTEGER NOT NULL,
            pay REAL NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE 
        )
    """)
    conn.commit()
    conn.close()


def add_employee(first_name, last_name, phone, email):
    conn = sqlite3.connect("employee_system.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT into employees (f_name, l_name, phone, email)
                            VALUES (?, ?, ?, ?)""",
                   (first_name, last_name, phone, email))
    conn.commit()
    conn.close()
    print(f"Added Employee {first_name} {last_name}")
