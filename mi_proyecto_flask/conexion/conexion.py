# clase de conexion a BD sin sqlalchemy 
import mysql.connector
from mysql.connector import Error

# conexion a la base de datos

def conexion():
    return mysql.connector.connect(
        host='192.168.10.114',
        database='desarrollo_web',
        user='root',  # luego en producción usa variable de entorno
        password='' # luego en producción usa variable de entorno
    )

# cerrar conexion a la base de datos

def cerrar_conexion(conn):
    if conn.is_connected():
        conn.close()
        print("Conexion a la base de datos cerrada.")