import psycopg2
from psycopg2.extras import DictCursor

class Movement:
    def __init__(self, employee_id, movement_type, amount, date, description=None, identifier=None):
        self.identifier = identifier
        self.employee_id = employee_id
        self.movement_type = movement_type
        self.amount = amount
        self.date = date
        self.description = description
    def insert_movement(self):
        try:
            if self.identifier is not None:
                print("Debes desasignar el id agregado del movimiento, de lo contrario no se podrá subir a la base de datos")
                return False
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    INSERT INTO movements (employee_id, movement_type, amount, date, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING employee_id;
                    """,
                    (
                        self.employee_id,
                        self.movement_type,
                        self.amount,
                        self.date,
                        self.description
                        )
                    )
                    self.employee_id = cursor.fetchone()
                    return True
        except Exception as e:
            print(f"Error inesperado {e}")


    @staticmethod
    def find_by_month(year: int, month: int):
        try:
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data_filter = f"{year:04d}-{month:02d}"
                    query = "SELECT * FROM movements WHERE TO_CHAR(date, 'YYYY-MM') = %s"
                    cursor.execute(query,(data_filter,))
                    return cursor.fetchall()
        except Exception as e:
            print("Error al buscar movimientos")
            return {}
        
    @staticmethod
    def find_by_date_range(start_date, end_date):
        try:
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    query = """
                            SELECT * FROM movements
                            WHERE date BETWEEN %s AND %s
                            """
                    cursor.execute(query,(start_date, end_date))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return {}
    @staticmethod
    def find_by_employee_and_month(employee_id: int, year: int, month: int):
        try:
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    data_filter = f"{year:04d}-{month:02d}"
                    query = "SELECT * FROM movements WHERE TO_CHAR(date, 'YYYY-MM') = %s AND employee_id = %s;"
                    cursor.execute(query,(data_filter,employee_id))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return {}


    @staticmethod
    def find_by_employee_and_date_range(employee_id: int, start_date, end_date):
        try:
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    query = """
                            SELECT * FROM movements
                            WHERE employee_id = %s AND (date BETWEEN %s AND %s);
                            """
                    cursor.execute(query,(employee_id, start_date, end_date))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return {}

    @staticmethod
    def delete_by_id(movement_id: int):
        try:
            with psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="*****",
                port= 5432
                ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM movements WHERE identifier = %s;", (movement_id,))
                    return True
        except Exception as e:
            print(f"Error de base de datos: {e}") 
            return False


