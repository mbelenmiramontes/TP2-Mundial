from flask import Blueprint, request, jsonify
import mysql.connector
from datetime import datetime
predicciones_bp = Blueprint('predicciones', __name__)

def obtener_coneccion():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="usuarios"
    )

@predicciones_bp.route("/partidos/<int:id>/prediccion/", methods=["POST"])
def post_predicciones(id):
    info_prediccion = request.get_json()

    if not info_prediccion or not 'id_usuario' in info_prediccion or not 'local' in info_prediccion or not 'visitante' in info_prediccion:
        error_400 = {
        "errors": [{
            "code": "400",
            "message": "Revisar JSON enviado, debe contener id, goles locales y goles visitantes.",
            "level": "error",
            "description": "Bad Request"
        }]
    } 
        return jsonify(error_400), 400
    id_usuario = info_prediccion.get('id_usuario')
    goles_local = info_prediccion.get('local')
    goles_visitante = info_prediccion.get('visitante')
    try:
        conn = obtener_coneccion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT fecha FROM partidos WHERE id = %s", [id])
        partido = cursor.fetchone()
        cursor.execute("SELECT id FROM predicciones WHERE id_partido = %s AND id_usuario = %s", (id, id_usuario))
        prediccion_previa = cursor.fetchone()
        if not partido:
            cursor.close()
            conn.close()
            error_404 = {
            "errors": [{
                    "code": "404",
                    "message": "Partido no encontrado",
                    "level": "error",
                    "description": "Not Found"
            }]
        }
            return jsonify(error_404), 404
        
        # datetime.now() hora actual
        if partido['fecha'] <= datetime.now() or prediccion_previa:
            cursor.close()
            conn.close()
            error_409 = {
                "errors": [{
                    "code": "409",
                    "message": "El partido ya comenzó o finalizó. O ya realizaste una predicción para este partido",
                    "level": "error",
                    "description": "Conflict"
                }]
            }
            return jsonify(error_409), 409

        query = """INSERT INTO predicciones (id_partido, id_usuario, goles_local, goles_visitante) 
                   VALUES (%s, %s, %s, %s)"""
        valores = (id, id_usuario, goles_local, goles_visitante)
        
        cursor.execute(query, valores)
        conn.commit() 

        cursor.close()
        conn.close()

        return jsonify({"message": "Predicción registrada."}), 201

    except Exception:
        error_500 = {
            "errors": [{
                "code": "500",
                "message": "Error al insertar en la base de datos",
                "level": "error",
                "description": "Internal Server Error"
            }]
        }
        return jsonify(error_500), 500