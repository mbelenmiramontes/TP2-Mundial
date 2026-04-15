from flask import jsonify
from datetime import datetime
from database.database import consultar_db, conectar_db, modificar_db

def mostrar_partidos(equipo, fecha, fase, limit, offset): #GET/PARTIDOS
    conn = conectar_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM partidos"
    condition = " WHERE 1=1" 
    params = []

    if fecha:
        condition += " AND fecha = %s"
        params.append(fecha)
    if equipo:
        condition += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.extend([equipo, equipo])
    if fase:
        condition += " AND fase = %s"
        params.append(fase.lower())
    
    cursor.execute("SELECT COUNT(*) as total FROM partidos " + condition, params)
    resultado_total = cursor.fetchone()
    total = resultado_total[0] if resultado_total else 0

    cursor.close()
    conn.close()
    
    params_paginados = params.copy()
    pagination = ""

    if limit:
        pagination += " LIMIT %s"
        params_paginados.append(limit)

    if offset is not None:
        pagination += " OFFSET %s"
        params_paginados.append(offset)
    
    query_final = sql + condition + pagination

    partidos = consultar_db(query_final, params_paginados)
    
    return partidos, total


def crear_partido(data): #POST/PARTIDOS
    try:
        if not data:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "JSON requerido"
            }]}), 400

        campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]
        for campo in campos:
            if campo not in data:
                return jsonify({ "errors": [{
                    "code": "400", 
                    "message": "Bad Request", 
                    "level": "error", 
                    "description": f"Falta el campo obligatorio: {campo}"
                }]}), 400
        
        data["equipo_local"] = data["equipo_local"].strip().title()
        data["equipo_visitante"] = data["equipo_visitante"].strip().title()

        if data["equipo_local"] == data["equipo_visitante"]:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "El equipo local y visitante no pueden ser el mismo"
            }]}), 400
        
        fase = data["fase"].strip().lower()
          
        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
        if fase not in fases_validas:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "Fase inválida"
            }]}), 400
          
        data["fase"] = fase
          
        try:
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d")
            data["fecha"] = fecha.strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Fecha inválida, usar YYYY-MM-DD"
            }]}), 400

        query_check = """
            SELECT id FROM partidos 
            WHERE equipo_local=%s AND equipo_visitante=%s AND fecha=%s
        """
        existente = consultar_db(query_check, (
            data["equipo_local"],
            data["equipo_visitante"],
            data["fecha"]
        ))

        if existente:
            return jsonify({ "errors": [{
                "code": "409", 
                "message": "Conflict", 
                "level": "error", 
                "description": "El partido ya existe"
            }]}), 409

        query_insert = """
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
            VALUES (%s, %s, %s, %s)
        """

        partido_id = modificar_db(query_insert, (
            data["equipo_local"],
            data["equipo_visitante"],
            data["fecha"],
            data["fase"]
        ))

        return jsonify({
            "mensaje": "Partido creado exitosamente",
            "id": partido_id
        }), 201

    except Exception as e:
        return jsonify({ "errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(e)
        }]}), 500


def actualizar_partido(id, data): #PUT/PARTIDOS/<ID>
    try:
        if not data:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "JSON requerido"
            }]}), 400

        campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]
        for campo in campos:
            if campo not in data:
                return jsonify({ "errors": [{
                    "code": "400",
                    "message": "Bad Request",
                    "level": "error",
                    "description": f"Falta el campo obligatorio: {campo}"
                }]}), 400

        if data["equipo_local"] == data["equipo_visitante"]:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El equipo local y visitante no pueden ser el mismo"
            }]}), 400

        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
        if data["fase"] not in fases_validas:
            return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Fase inválida"
            }]}), 400

        partido_existente = consultar_db("SELECT id FROM partidos WHERE id = %s", (id,))
        if not partido_existente:
            return jsonify({ "errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": "El partido no existe"
            }]}), 404

        query_check = """
            SELECT id FROM partidos
            WHERE equipo_local=%s AND equipo_visitante=%s AND fecha=%s AND id != %s
        """
        duplicado = consultar_db(query_check, (
            data["equipo_local"], data["equipo_visitante"], data["fecha"], id
        ))

        if duplicado:
            return jsonify({ "errors": [{
                "code": "409",
                "message": "Conflict",
                "level": "error",
                "description": "Ya existe otro partido con esos equipos en esa fecha"
            }]}), 409
        
        query_update = """
            UPDATE partidos
            SET equipo_local=%s, equipo_visitante=%s, fecha=%s, fase=%s
            WHERE id=%s
        """
        modificar_db(query_update, (
            data["equipo_local"], data["equipo_visitante"], data["fecha"], data["fase"], id
        ))

        return '', 204

    except Exception as e:
        return jsonify({ "errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(e)
        }]}), 500


def actualizar_partido_id(id, data): #PATCH/PARTIDOS/<ID>
    partido = consultar_db("SELECT * FROM partidos WHERE id = %s", (id,))
    if not partido:
        return None
    
    campos = []
    parametros = []

    for campo, valor in data.items():
        campos.append(f"{campo} = %s")
        parametros.append(valor)

    parametros.append(id)
    sql = f"UPDATE partidos SET {', '.join(campos)} WHERE id = %s"
    modificar_db(sql, parametros)
    return True