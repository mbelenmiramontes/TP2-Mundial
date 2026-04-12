from flask import Blueprint, request, jsonify
from database.database import conectar_db
from datetime import datetime

predicciones_bp = Blueprint('predicciones', __name__)

@predicciones_bp.route("/partidos/<int:id>/prediccion/", methods=["POST"])
def post_predicciones(id): #REGISTRAR UNA PREDICCIÓN PARA UN PARTIDO
    info_prediccion = request.get_json()

    if not info_prediccion or 'id_usuario' not in info_prediccion or 'local' not in info_prediccion or 'visitante' not in info_prediccion:
        return jsonify({ "errors": [{
            "code": "400",
            "message": "Bad Request",
            "level": "error",
            "description": "El JSON debe contener id_usuario, local (goles) y visitante (goles)."
        }]}), 400
    

    id_usuario = info_prediccion.get('id_usuario')
    goles_local = info_prediccion.get('local')
    goles_visitante = info_prediccion.get('visitante')

    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT fecha FROM partidos WHERE id = %s", [id])
        partido = cursor.fetchone()

        if not partido:
            cursor.close()
            conn.close()
            return jsonify({ "errors": [{
                    "code": "404",
                    "message": "Not Found",
                    "level": "error",
                    "description": "El partido no existe"
                }]}), 404

        cursor.execute("SELECT id FROM predicciones WHERE id_partido = %s AND id_usuario = %s", (id, id_usuario))
        prediccion_previa = cursor.fetchone()
        
        # datetime.now() hora actual / ProDe
        if partido['fecha'] <= datetime.now() or prediccion_previa:
            cursor.close()
            conn.close()
            return jsonify({ "errors": [{
                    "code": "409",
                    "message": "Conflict",
                    "level": "error",
                    "description": "El partido ya comenzó o finalizó. O ya realizaste una predicción para este partido"
                }]}), 409

        query = """INSERT INTO predicciones (id_partido, id_usuario, goles_local, goles_visitante) 
                   VALUES (%s, %s, %s, %s)"""
        valores = (id, id_usuario, goles_local, goles_visitante)
        
        cursor.execute(query, valores)
        conn.commit() 

        cursor.close()
        conn.close()

        return jsonify({"message": "Predicción registrada correctamente."}), 201

    except Exception as e:
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500