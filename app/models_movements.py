import sqlite3

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
            conn = sqlite3.connect("db/vidrieria.db")
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
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def find_by_month(year: int, month: int):
        try:
            conn = sqlite3.connect("db/vidrieria.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            data_filter = f"{year:04d}-{month:02d}"
            query = "SELECT * FROM Movement WHERE strftime('%Y-%m', date) = ?"

            cursor.execute(query,(data_filter,))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error al buscar movimientos")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    def find_by_employee_and_month(employee_id: int, year: int, month: int):
        try:
            conn = sqlite3.connect("db/vidrieria.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            data_filter = f"{year:04d}-{month:02d}"
            query = "SELECT * FROM Movement WHERE strftime('%Y-%m', date) = ? AND employee_id = ?"

            cursor.execute(query,(data_filter,employee_id))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error al buscar movimientos")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete_by_id(movement_id: int):
        try:
            conn = sqlite3.connect("db/vidrieria.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Movement WHERE identifier = ?", (movement_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error específico al eliminar movimiento: {e}") 
            return False
        finally:
            if conn:
                conn.close()

