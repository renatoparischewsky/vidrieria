import sqlite3

conn = sqlite3.connect("db/vidreria.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employee (
            identifier INTEGER PRIMARY KEY AUTOINCREMENT,
            tax_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            base_salary INTEGER NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0,1))
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Movement (
            identifier INTEGER PRIMARY KEY AUTOINCREMENT,   
            employee_id INTEGER NOT NULL,   
            movement_type TEXT NOT NULL,   
            amount INT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (employee_id) REFERENCES Employee(identifier)
)               
""")

conn.commit()
conn.close()