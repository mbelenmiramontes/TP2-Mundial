from flask import Blueprint, request, jsonify, url_for
from backend.controller.match_controller import mostrar_partidos
match_bp = Blueprint('match', __name__)
@match_bp.route("/partidos", methods=["GET"])
def listar_partidos():
    equipo = request.args.get('equipo')
    fecha = request.args.get('fecha')
    fase = request.args.get('fase')
    limit = request.args.get('_limit', 10,type=int)
    offset = request.args.get('_offset', 0,type=int)
    
    partidos, total = mostrar_partidos(equipo, fecha, fase, limit, offset)
    
    last = max(0, (int(total) - 1) // limit) * limit
    links = {
        "_first": {"href": url_for('match.listar_partidos', _limit=limit, _offset=0)},
        "_prev": {"href": url_for('match.listar_partidos', _limit=limit, _offset=max(0, offset - limit))} if offset > 0 else None,
        "_next": {"href": url_for('match.listar_partidos', _limit=limit, _offset=offset + limit)} if offset + limit < total else None,
        "_last": {"href": url_for('match.listar_partidos', _limit=limit, _offset=last)}
    }
    
    return jsonify({"partidos": partidos, "_links": links}), 200



