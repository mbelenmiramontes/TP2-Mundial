from flask import Blueprint, request, jsonify
import mysql.connector
from backend.database.database import conectar_db 
from backend.controller.match_controller import mostrar_partidos
match_bp = Blueprint('match', __name__)
@match_bp.route("/partidos", methods=["GET"])
def procesar_partido():
    equipo = request.args.get('equipo')
    fecha = request.args.get('fecha')
    fase = request.args.get('fase')
    partidos = mostrar_partidos(equipo, fecha, fase)
    return jsonify(partidos)



