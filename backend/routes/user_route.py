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
                "code": "404",
                "message": "No se encontró el usuario",
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

@usuario_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    data=request.get_json()

    if not data:
        return jsonify({"error": "No se completaron los datos."}), 400
    
    nombre=data.get("nombre")
    email=data.get("email")

    if not nombre or not email:
        return jsonify({"error": "Falta un dato obligatorio. "}), 400
    
    nuevo_usuario = {
        "nombre":nombre,
        "email":email
    }

    return jsonify(nuevo_usuario),201
    
