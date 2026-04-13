from flask import Blueprint, request, jsonify
from controller.user_controller import get_usuarios
from database.database import conectar_db, modificar_db, consultar_db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route("/usuarios", methods=["GET"])
#LISTAR USUARIOS
def listar_usuarios():
    try:
        limit = int(request.args.get("_limit", 10))
        offset = int(request.args.get("_offset", 0))

        if limit < 1:
            return jsonify({ "errors": [{
                    "code": "400", 
                    "message": "Bad request", 
                    "level": "error", 
                    "description": "El limit debe ser mayor a 0"
                }]}), 400
        
        if offset < 0:
            return jsonify({ "errors": [{
                    "code": "400", 
                    "message": "Bad request", 
                    "level": "error", 
                    "description": "El offset debe ser mayor o igual a 0"
                }]}), 400
        response = get_usuarios(request)

        if not response.get_json().get("usuarios"):
            return '', 204
        
        return response, 200
    
    except Exception as error:
        return jsonify({ "errors": [{
                "code": "500", 
                "message": "Internal Server Error", 
                "level": "error", 
                "description": str(error)
            }]}), 500


@usuario_bp.route("/usuarios/<int:id>", methods=["GET"])
def listar_usuario_id(id): #OBTENER USUARIO POR ID
    if id <= 0:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
    
    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE id = %s"

        cursor.execute(query, [id])
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return jsonify({
                "id": usuario["id"],
                "nombre": usuario["nombre"],
                "email": usuario["email"],
            }), 200
        
        if not usuario:
            return jsonify({
            "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "No se encontró un usuario con el ID proporcionado"
            }]}), 404
        
    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": "INTERNAL_SERVER_ERROR"
            }]}), 500


@usuario_bp.route("/usuarios", methods=["POST"])
def crear_usuario(): #CREAR USUARIO
    data = request.get_json()

    if not data:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "No se completaron los datos"
            }]}), 400
    
    nombre = data.get("nombre")
    email = data.get("email")

    if not nombre or not email:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Falta un dato obligatorio: nombre y email son requeridos"
            }]}), 400
    
    try:
        query = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
        params = (nombre, email)
        nuevo_id = modificar_db(query, params)
        return jsonify({"id": nuevo_id}), 201

    except Exception as e:
        if "Duplicate entry" in str(e): #POR SI EL EMAIL YA EXISTE
            return jsonify({ "errors": [{
                    "code": "409",
                    "message": "Conflict",
                    "level": "error",
                    "description": "El email ya se encuentra registrado"
                }]}), 409
            
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500

@usuario_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def borrar_usuario(id): #BORRAR USUARIO
    if id <= 0:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]}), 400

    try:

        usuario = consultar_db("SELECT id FROM usuarios WHERE id = %s", (id,))

        if not usuario:
            return jsonify({ "errors": [{
                    "code": "404",
                    "message": "Not Found",
                    "level": "error",
                    "description": "No existe un usuario con el ID proporcionado."
                }]}), 404

        modificar_db("DELETE FROM usuarios WHERE id = %s", (id,))

        return '', 204
    
    except Exception as e:
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500