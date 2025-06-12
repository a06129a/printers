# conexion_bd.py
import sqlite3
import os
import sys

def obtener_ruta_db():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "my_base.db")
    return os.path.join(os.path.abspath("."), "my_base.db")

def get_connection():
    try:
        ruta_db = obtener_ruta_db()
        connection = sqlite3.connect(ruta_db)
        return connection
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos SQLite:", e)
        return None
