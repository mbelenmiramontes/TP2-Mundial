from flask import Blueprint, request, jsonify
import mysql.connector
match_bp = Blueprint('match', __name__)
@match_bp.route("/partido", methods=["GET", "POST"])
def obtener_coneccion():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="partidos"
    )


def procesar_partido():
    if request.method == "GET":
        conn = obtener_coneccion()
        cursor = conn.cursor()
        sql = "SELECT * FROM partido" #cambiar nombre de sql si se cambia
        cursor.execute(sql)
        partidos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(partidos)
    elif request.method == "POST":
        conn = obtener_coneccion()
        cursor = conn.cursor()

