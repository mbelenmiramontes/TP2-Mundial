from flask import Blueprint, request, jsonify
from controller.user_controller import get_users
import mysql.connector

usuario_bp = Blueprint('usuario', __name__)

def obtener_coneccion():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="usuarios"
    )
  
@usuario_bp.route("/usuarios", methods=["GET"])
def list_users():
    return get_users(request)

@usuario_bp.route("/usuario/<int:id>", methods=["GET"])
def get_usuario(id):
    if id <= 0:
        error_400 = {
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "ID inválido",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]
        }
        return jsonify(error_400), 400
    try:
        conn = obtener_coneccion()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE id = %s"

        cursor.execute(query, [id])
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            respuesta = {
                "id": usuario["id"],
                "nombre": usuario["nombre"],
                "email": usuario["email"],
            }
            return jsonify(respuesta), 200
        if not usuario:
            mensaje_error_404 = {
            "errors": [{
                "code": "NOT_FOUND",
                "message": "No se encontró el usuario",
                "level": "error",
                "description": f"El {id} no se encuentra en la base de datos."
            }]
        }
            return jsonify(mensaje_error_404), 404
    except Exception:
        error_500 = {
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Error interno del servidor",
                "level": "error",
                "description": "Hay problemas en el servidor"
            }]
        }
        return jsonify(error_500), 500
    
