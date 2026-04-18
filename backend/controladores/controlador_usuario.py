from flask import jsonify, url_for
from database.database import consultar_db

def get_usuarios(request):
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    query = "SELECT id, nombre, email FROM usuarios LIMIT %s OFFSET %s"
    params = (limit, offset)
    result = consultar_db(query, params)

    count_query = "SELECT COUNT(*) as total FROM usuarios"
    total_res = consultar_db(count_query)
    total = total_res[0]["total"] if total_res else 0

    last_offset = max(0, ((total - 1) // limit) * limit)

    links = {
        "_first": {"href": url_for("usuario.listar_usuarios", _limit=limit, _offset=0, _external=True)},
        "_last": {"href": url_for("usuario.listar_usuarios", _limit=limit, _offset=last_offset, _external=True)}
    }

    if offset > 0:
        prev_off = max(0, offset - limit)
        links["_prev"] = {"href": url_for("usuario.listar_usuarios", _limit=limit, _offset=prev_off, _external=True)}

    if offset + limit < total:
        links["_next"] = {"href": url_for("usuario.listar_usuarios", _limit=limit, _offset=offset + limit, _external=True)}


    return jsonify({"usuarios": result, "_links": links})