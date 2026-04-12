from flask import jsonify, request
from database.database import consultar_db

def get_usuarios(request): #GET/USUARIOS
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    query = "SELECT id, nombre, email FROM usuarios LIMIT %s OFFSET %s"
    params = (limit, offset)

    result = consultar_db(query, params)

    count_query = "SELECT COUNT(*) as total FROM usuarios"
    total_res = consultar_db(count_query)
    total = total_res[0]["total"] if total_res else 0

    last_offset = max(0, ((total - 1) // limit) * limit)

    users_response = {
        "usuarios": result,
        "_links": {
            "_first": {"href": f"/usuarios?_limit={limit}&_offset=0"},
            "_last": {"href": f"/usuarios?_limit={limit}&_offset={last_offset}"}
        }
    }

    if offset > 0:
        prev_off = max(0, offset - limit)
        users_response["_links"]["_prev"] = {"href": f"/usuarios?_limit={limit}&_offset={prev_off}"}
    
    if offset + limit < total:
        users_response["_links"]["_next"] = {"href": f"/usuarios?_limit={limit}&_offset={offset + limit}"}

    return jsonify(users_response)