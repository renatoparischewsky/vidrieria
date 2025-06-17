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

conn.commit()

conn.close()