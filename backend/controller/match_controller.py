#match controller codigo aca
from flask import jsonify
from database.database import consultar_db, modificar_db

def crear_partido(data):
    try:
        if not data:
            return jsonify({"error": "JSON requerido"}), 400

        campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]
        for campo in campos:
            if campo not in data:
                return jsonify({"error": f"Falta {campo}"}), 400

        data["equipo_local"] = data["equipo_local"].strip().title()
        data["equipo_visitante"] = data["equipo_visitante"].strip().title()
        
        if data["equipo_local"] == data["equipo_visitante"]:
            return jsonify({"error": "Equipos iguales"}), 400

        fase = data["fase"].strip().lower()
        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
       
        if fase not in fases_validas:
            return jsonify({"error": "Fase inválida"}), 400
        
        data["fase"] = fase

        try:
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d")
            data["fecha"] = fecha.strftime("%Y-%m-%d")
        except:
            return jsonify({"error": "Fecha inválida, usar YYYY-MM-DD"}), 400

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
            return jsonify({"error": "El partido ya existe"}), 409

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
            "mensaje": "Partido creado",
            "id": partido_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
