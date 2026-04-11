from flask import Blueprint, request, jsonify, url_for
from backend.controller.match_controller import mostrar_partidos
from backend.database.database import conectar_db

match_bp = Blueprint('match', __name__)

@match_bp.route("/partidos", methods=["GET"])
def listar_partidos(): #LISTAR PARTIDOS
    try:
        equipo = request.args.get('equipo')
        fecha = request.args.get('fecha')
        fase = request.args.get('fase')
        limit = request.args.get('_limit', 10,type=int)
        offset = request.args.get('_offset', 0,type=int)
        
        #Validaciones
        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
        if fase and fase.lower() not in fases_validas:
            return jsonify({"errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": f"La fase debe ser una de: {', '.join(fases_validas)}"
            }]}), 400
        
        if limit < 1:
            return jsonify({"errors": [{
                "code": "400", 
                "message": "Bad request", 
                "level": "error", 
                "description": "El limit debe ser mayor a 0"
            }]}), 400

        if offset < 0:
            return jsonify({"errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "El offset no puede ser negativo"
            }]}), 400

        partidos, total = mostrar_partidos(equipo, fecha, fase, limit, offset)

        if not partidos:
            return '', 204 #Si no hay resultados
        
        last = max(0, (int(total) - 1) // limit) * limit

        links = {
            "_first": {"href": url_for('match.listar_partidos', _limit=limit, _offset=0, _external=True)},
            "_last": {"href": url_for('match.listar_partidos', _limit=limit, _offset=last, _external=True)}
        }

        if offset > 0:
            links["_prev"] = {"href": url_for('match.listar_partidos', _limit=limit, _offset=max(0, offset - limit), _external=True)}
        
        if offset + limit < total:
            links["_next"] = {"href": url_for('match.listar_partidos', _limit=limit, _offset=offset + limit, _external=True)}
        
        return jsonify({"partidos": partidos, "_links": links}), 200
    
    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500


@match_bp.route("/partidos/<int:id>", methods=["GET"])
def get_partido(id): #OBTENER PARTIDO POR ID
    if id <= 0:
        return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número positivo."
            }]}), 400
    
    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                p.id, p.equipo_local, p.equipo_visitante, p.fecha, p.fase,
                r.goles_local, r.goles_visitante
            FROM partidos p
            LEFT JOIN resultados r ON p.id = r.id_partido
            WHERE p.id = %s
        """
        cursor.execute(query, [id])
        partido = cursor.fetchone()

        cursor.close()
        conn.close()

        if partido:
            respuesta = {
                "id": partido["id"],
                "equipo_local": partido["equipo_local"],
                "equipo_visitante": partido["equipo_visitante"],
                "fecha": partido["fecha"].isoformat() if partido["fecha"] else None,
                "fase": partido["fase"].upper() if partido ["fase"] else None,
                "resultado": None # Por defecto es None
            }

            if partido["goles_local"] is not None:
                respuesta["resultado"] = {
                    "local": partido["goles_local"],
                    "visitante": partido["goles_visitante"]
                }
            return jsonify(respuesta), 200
        
        return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "El partido solicitado no existe."
            }]}), 404
    
    except Exception as e:
        return jsonify({"errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500


@match_bp.route("/partidos/<int:id>", methods=["DELETE"])
def borrar_partido(id): #ELIMINAR PARTIDO
    if id <= 0:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]}), 400
    
    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM partidos WHERE id = %s"
        cursor.execute(query, [id])
        partido = cursor.fetchone()

        if partido is None:
            return jsonify({ "errors": [{
                    "code": "404",
                    "message": "Not Found",
                    "level": "error",
                    "description": "No existe un partido con el ID proporcionado."
                }]}), 404

        query = "DELETE FROM partidos WHERE id = %s"
        cursor.execute(query, [id])
        conn.commit()

        return '', 204

    except Exception as e:
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()