import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
host=os.getenv("DB_HOST"),
dbname=os.getenv("DB_NAME"),
user=os.getenv("DB_USER"),
password=os.getenv("DB_PASSWORD"),
port=os.getenv("DB_PORT")
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