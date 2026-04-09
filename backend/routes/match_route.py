from flask import Blueprint, request, jsonify
import mysql.connector
from backend.database.database import conectar_db 
match_bp = Blueprint('match', __name__)
@match_bp.route("/partidos", methods=["GET", "POST"])
def procesar_partido():
    if request.method == "GET":
        conn = conectar_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM partidos" 
        cursor.execute(sql)
        partidos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(partidos)
    elif request.method == "POST":


