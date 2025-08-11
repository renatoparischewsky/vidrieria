import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class Employee:
    def __init__(self, tax_id=None, first_name=None, last_name=None, base_salary=None, is_active: bool = True, employee_id=None):
        self.employee_id = employee_id
        self.tax_id = tax_id
        self.first_name = first_name
        self.last_name = last_name
        self.base_salary = base_salary
        self.is_active = is_active

    @classmethod
    def load_employee(cls, employee_id):
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""
                    SELECT * FROM employees                    
                    WHERE employee_id = %s;                    
                    """, (employee_id,)
                    ) # the comma after the variable employee_id is because I need to input a tuple as an argument, and without the comma is just an expression with brackets
                    row = cursor.fetchone()
                    if row is None: # So, there was no record found.
                        print(f"Empleado con id {employee_id} no existe actualmente.")
                        return {}
                    return cls(
                        employee_id=row['employee_id'],
                        tax_id=row['tax_id'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        base_salary=row['base_salary'],
                        is_active=row['is_active']
                    )
        except Exception as e:
            print(f"Error inesperado {e}")
            return {}


    def insert_employee(self):
        if self.employee_id is not None:
            print("Debes desasignar el id agregado del empleado, de lo contrario no se podrá subir a la base de datos")
            return False
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""
                    INSERT INTO employees (tax_id, first_name, last_name, base_salary, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING employee_id;
                    """,
                    (
                        self.tax_id,
                        self.first_name,
                        self.last_name, 
                        self.base_salary,
                        self.is_active
                        )
                    )
                    self.employee_id = cursor.fetchone()
                    return True
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return False

    @staticmethod
    def get_all_active():
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("SELECT employee_id, tax_id, first_name, last_name, base_salary FROM employees WHERE is_active = True ORDER BY last_name")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []



    @staticmethod
    def get_all_inactive():
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("SELECT employee_id, tax_id, first_name, last_name, base_salary FROM employees WHERE is_active = False ORDER BY last_name")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []


    @staticmethod
    def get_all_employees():
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("SELECT employee_id, tax_id, first_name, last_name, base_salary FROM employees ORDER BY last_name;")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []


    def mark_as_inactive(self):
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    UPDATE employees
                    SET is_active = False
                    WHERE employee_id = %s
                    RETURNING is_active;
                    """,
                    (self.employee_id,)
                    )
                    self.employee_id = cursor.fetchone()
                    return True
        except Exception as e:
            print(f"Error de base de datos: {e}")

    def mark_as_active(self):
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    UPDATE employees
                    SET is_active = True
                    WHERE employee_id = %s
                    RETURNING is_active;
                    """,
                    (self.employee_id,)
                    )
                    self.employee_id = cursor.fetchone()
                    return True
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return False

    def update_employee(self):
        if self.employee_id is None:
            return False
        try:
            with psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
                ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE employees
                        SET tax_id = %s, first_name = %s, last_name = %s, base_salary = %s, is_active = %s
                        WHERE employee_id = %s
                    """, (
                        self.tax_id, self.first_name, self.last_name, 
                        self.base_salary, self.is_active, self.employee_id
                    )
                    )
                    return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            return False