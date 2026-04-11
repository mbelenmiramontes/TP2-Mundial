from flask import jsonify, request
from database.database import consultar_db

def get_users(request):
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    query = "SELECT id, name, email FROM users LIMIT %s OFFSET %s"
    params = (limit, offset)

    result = consultar_db(query, params)

    count = "SELECT COUNT(*) as total FROM users"
    total = consultar_db(count)[0]["total"]

    last_offset = (total // limit) * limit

    users = {
        "users" : result,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "first": f"/usuarios?limit={limit}&offset=0",
            "next": f"/usuarios?limit={limit}&offset={offset + limit}",
            "previous": f"/usuarios?limit={limit}&offset={max(0, offset - limit)}",
            "last": f"/usuarios?limit={limit}&offset={last_offset}"
        
        }
    }
    return jsonify(users)