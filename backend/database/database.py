import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # pongan su contraseña
    'database': 'database_tpbackend' 
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def execute_query(query, params=None): #SELECT
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        resultados = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    return resultados

def execute_commit(query, params=None): #INSERT, UPDATE, DELETE
    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute(query, params or ())
        conexion.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conexion.close()