from flask import Blueprint, request, jsonify, url_for
from backend.controller.match_controller import mostrar_partidos
match_bp = Blueprint('match', __name__)
@match_bp.route("/partidos", methods=["GET"])
def listar_partidos():
    try:
        equipo = request.args.get('equipo')
        fecha = request.args.get('fecha')
        fase = request.args.get('fase')
        limit = request.args.get('_limit', 10,type=int)
        offset = request.args.get('_offset', 0,type=int)
        
        #validaciones
        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
        if fase and fase.lower not in fases_validas:
            return jsonify({"errors": [{"code": "400", "message": "Fase Invalida", "level": "error", "description": f"La fase debe ser una de: {', '.join(fases_validas)}"}}]}), 400
        
        if limit < 1:
            return jsonify({"errors": [{"code": "400", "message": "Limit inválido", "level": "error", "description": "El limit debe ser mayor a 0"}]}), 400

        if offset < 0:
            return jsonify({"errors": [{"code": "400", "message": "Offset inválido", "level": "error", "description": "El offset no puede ser negativo"}]}), 400

        partidos, total = mostrar_partidos(equipo, fecha, fase, limit, offset)

        if not partidos:
            return '', 204 #Si no hay resultados
        
        last = max(0, (int(total) - 1) // limit) * limit
        links = {
            "_first": {"href": url_for('match.listar_partidos', _limit=limit, _offset=0)},
            "_prev": {"href": url_for('match.listar_partidos', _limit=limit, _offset=max(0, offset - limit))} if offset > 0 else None,
            "_next": {"href": url_for('match.listar_partidos', _limit=limit, _offset=offset + limit)} if offset + limit < total else None,
            "_last": {"href": url_for('match.listar_partidos', _limit=limit, _offset=last)}
        }
        
        return jsonify({"partidos": partidos, "_links": links}), 200
    except Exception as error:
        return jsonify({"errors": [{"code":  "500", "message": "Error interno", "level": "error", "description": str(error)}]}), 500


