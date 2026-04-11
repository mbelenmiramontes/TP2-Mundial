from flask import Blueprint, request, jsonify
import mysql.connector
match_bp = Blueprint('partido', __name__)

def obtener_db():
    return mysql.connector.connect(
        host ="localhost",
        user="admin",
        password="admin",
        database="usuarios"

    )

@match_bp.route("/partidos/<int:id>", methods=["DELETE"])
def borrar_partido(id):
    if id <= 0:
        error_400 = {
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "ID invalido",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]
        }   
        return jsonify(error_400), 400
    try:
        conn = obtener_db()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM partidos WHERE id = %s"
        cursor.execute(query, [id])
        partido = cursor.fetchone()

        if partido is None:
            error_404 = {
                "errors": [{
                    "code": "NOT_FOUND",
                    "message": "Partido no encontrado",
                    "level": "error",
                    "description": "No existe un partido con el ID proporcionado."
                }]
            }
            return jsonify(error_404), 404

        query = "DELETE FROM partidos WHERE id = %s"
        cursor.execute(query, [id])
        conn.commit()

        return jsonify({"message": "Partido eliminado correctamente"}), 200

    except Exception as e:
        error_500 = {
            "errors": [{
                "code": "INTERNAL_ERROR",
                "message": "Error interno del servidor",
                "level": "error",
                "description": str(e)
            }]
        }
        return jsonify(error_500), 500

    finally:
        cursor.close()
        conn.close()
    





