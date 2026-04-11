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

@match_bp.route("/partido/<int:id>", methods=["GET"])
def get_partido(id):
    if id <= 0:
        error_400 = {
            "errors": [{
                "code": "400",
                "message": "ID inválido",
                "level": "error",
                "description": "BAD_REQUEST"
            }]
        }
        return jsonify(error_400), 400
    try:
        conn = obtener_coneccion()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                p.id, p.equipo_local, p.equipo_visitante, p.fecha, p.fase,
                r.goles_local, r.goles_visitante
            FROM partidos p
            LEFT JOIN resultados r ON p.id = r.id_partido
            WHERE p.id = %s
        """


        cursor.execute(query, [id])
        partido = cursor.fetchone()
        cursor.close()
        conn.close()
        if partido:
            respuesta = {
                "id": partido["id"],
                "equipo_local": partido["equipo_local"],
                "equipo_visitante": partido["equipo_visitante"],
                "fecha": partido["fecha"].isoformat() if partido["fecha"] else None,
                "fase": partido["fase"],
                "resultado": None 
            }
            if partido["goles_local"] is not None:
                respuesta["resultado"] = {
                    "local": partido["goles_local"],
                    "visitante": partido["goles_visitante"]
                }
            return jsonify(respuesta), 200
        if not partido:
            mensaje_error_404 = {
            "errors": [{
                "code": "404",
                "message": "No se encontró el partido",
                "level": "error",
                "description": "NOT_FOUND"
            }]
        }
            return jsonify(mensaje_error_404), 404
    except Exception:
        error_500 = {
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": "INTERNAL_SERVER_ERROR"
            }]
        }
        return jsonify(error_500), 500
    
