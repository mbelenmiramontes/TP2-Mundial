from flask import jsonify, url_for
from database.database import consultar_db
from collections import defaultdict

def get_ranking(limit, offset):
    query = """
        SELECT
            usuarios.id AS id_usuario,
            usuarios.nombre,
            predicciones.goles_local AS goles_local,
            predicciones.goles_visitante AS pred_visitante,
            resultados.goles_local AS real_local,
            resultados.goles_visitante AS real_visitante
        FROM usuarios
        INNER JOIN predicciones ON usuarios.id = predicciones.id_usuario
        INNER JOIN resultados ON predicciones.id_partido = resultados.id_partido
"""

    rows = consultar_db(query)

    puntos_usuarios = defaultdict(int)
    for row in rows:
        pred_local = row["goles_local"]
        pred_visitante = row["pred_visitante"]
        real_local = row["real_local"]
        real_visitante = row["real_visitante"]

        if pred_local == real_local and pred_visitante == real_visitante:
            puntos = 3
        elif (pred_local > pred_visitante and real_local > real_visitante) or (pred_local < pred_visitante and real_local < real_visitante):
            puntos = 1
        elif pred_local == pred_visitante and real_local == real_visitante:
            puntos = 1
        else:
            puntos = 0

        puntos_usuarios[row["id_usuario"]] += puntos

    listado_ranking = [{"id_usuario": userID, "puntos": points}
                        for userID, points in puntos_usuarios.items()]
    listado_ranking.sort(key=lambda x: x["puntos"], reverse=True)

    total = len(listado_ranking)
    last_offset = max(0, ((total - 1) // limit) * limit)
    top_ranking = listado_ranking[offset:offset + limit]

    links = {
            "_first": {"href": url_for("ranking.obtener_ranking", _limit=limit, _offset=0, _external=True)},
            "_last": {"href": url_for("ranking.obtener_ranking", _limit=limit, _offset=last_offset, _external=True)},
        }
    
    if offset > 0:
        links["prev"] = {"href": url_for("ranking.obtener_ranking", _limit=limit, _offset=max(0, offset - limit), _external=True)}
    if offset + limit < total:
        links["next"] = {"href": url_for("ranking.obtener_ranking", _limit=limit, _offset=offset + limit, _external=True)}


    return jsonify({"ranking": top_ranking, "_links": links})