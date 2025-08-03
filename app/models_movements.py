import sqlite3
from datetime import date

class Movement:
    def __init__(self, employee_id, movement_type, amount, date, description=None, identifier = None):
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
            with sqlite3.connect("db/vidrieria.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO Movement (employee_id, movement_type, amount, date, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.employee_id,
                    self.movement_type,
                    self.amount,
                    self.date,
                    self.description
                ))

                self.identifier = cursor.lastrowid
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inesperado {e}")


    @staticmethod
    def find_by_month(year: int, month: int):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                data_filter = f"{year:04d}-{month:02d}"
                query = "SELECT * FROM Movement WHERE strftime('%Y-%m', date) = ?"

                cursor.execute(query,(data_filter,))
                return cursor.fetchall()
        except Exception as e:
            print("Error al buscar movimientos")
            return []
        
    @staticmethod
    def find_by_date_range(start_date, end_date):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = """
                        SELECT * FROM Movement
                        WHERE date BETWEEN ? AND ?
                        """
                
                start_date_f = start_date.isoformat()
                end_date_f = end_date.isoformat()
                cursor.execute(query,(start_date_f, end_date_f))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return []
    @staticmethod
    def find_by_employee_and_month(employee_id: int, year: int, month: int):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                data_filter = f"{year:04d}-{month:02d}"
                query = "SELECT * FROM Movement WHERE strftime('%Y-%m', date) = ? AND employee_id = ?"

                cursor.execute(query,(data_filter,employee_id))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []


    @staticmethod
    def find_by_employee_and_date_range(employee_id: int, start_date, end_date):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = """
                        SELECT * FROM Movement
                        WHERE employee_id = ? AND (date BETWEEN ? AND ?)
                        """
                
                start_date_f = start_date.isoformat()
                end_date_f = end_date.isoformat()
                cursor.execute(query,(employee_id, start_date_f, end_date_f))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return []

    @staticmethod
    def delete_by_id(movement_id: int):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Movement WHERE identifier = ?", (movement_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error de base de datos: {e}") 
            return False


