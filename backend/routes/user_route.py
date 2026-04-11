from flask import Blueprint, request, jsonify

user_bp=Blueprint('user',__name__)

@user_bp.route("/usuarios", methods=["POST"])
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


    


