import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="*****",
    port= 5432
    )
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    identifier SERIAL PRIMARY KEY,
    tax_id VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    base_salary NUMERIC(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Movement (
    identifier SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES Employee(identifier),
    movement_type VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    date DATE NOT NULL,
    description TEXT
);
""")

conn.commit()
conn.close()