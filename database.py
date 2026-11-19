
import sqlite3

def obtener_conexion():
    conexion = sqlite3.connect("contactos.db")
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tabla():
    conexion = obtener_conexion()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT,
            categoria TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

