import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')

db_config = {
    'host': 'localhost',
    'user': db_user,
    'password': db_password,
    'database': 'database_tpbackend' 
}

def conectar_db():
    conn = mysql.connector.connect(**db_config)
    return conn


def consultar_db(query, params=None): #GET(SELECT)
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        resultados = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    return resultados

def modificar_db(query, params=None): # POST(INSERT), PUT/PATCH(UPDATE), DELETE(DELETE)
    conexion = conectar_db()
    cursor = conexion.cursor()

    try:
        cursor.execute(query, params or ())
        conexion.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conexion.close()