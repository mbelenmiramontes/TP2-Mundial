from flask import Blueprint, request, jsonify
from controladores.controlador_ranking import get_ranking

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route("/ranking", methods=["GET"])

def obtener_ranking():
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
        response = get_ranking(limit, offset)

        if not response.get_json().get("ranking"):
            return '', 204
        
        return response, 200
    
    except Exception as error:
        return jsonify({ "errors": [{
                "code": "500", 
                "message": "Internal Server Error", 
                "level": "error", 
                "description": str(error)
            }]}), 500