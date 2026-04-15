from flask import jsonify
from database.database import consultar_db, conectar_db

def cargar_resultado(id, data): #PUT/PARTIDOS/<ID>/RESULTADOS
    try:
        if not data or 'local' not in data or 'visitante' not in data:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El JSON debe contener goles_local y goles_visitante."
            }]}), 400

        goles_local = data['local']
        goles_visitante = data['visitante']

        if not isinstance(goles_local, int) or not isinstance(goles_visitante, int):
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los goles deben ser números enteros."
            }]}), 400

        if goles_local < 0 or goles_visitante < 0:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los goles no pueden ser negativos."
            }]}), 400

        partido_existente = consultar_db("SELECT id FROM partidos WHERE id = %s", (id,))
        if not partido_existente:
            return jsonify({ "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "El partido no existe."
            }]}), 404

        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO resultados (id_partido, goles_local, goles_visitante)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE goles_local=%s, goles_visitante=%s
        """
        cursor.execute(query, (id, goles_local, goles_visitante, goles_local, goles_visitante))
        conn.commit()

        cursor.close()
        conn.close()

        return '', 204

    except Exception as e:
        return jsonify({ "errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(e)
        }]}), 500
