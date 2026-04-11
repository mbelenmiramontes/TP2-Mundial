#match controller codigo aca
import mysql.connector
from flask import jsonify

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="asantosv",
        password="1234",
        database="prode"
    )

def crear_partido(data):
    try:
        # Validación (400)
        if not data:
            return jsonify({"error": "JSON requerido"}), 400

        campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]
        for campo in campos:
            if campo not in data:
                return jsonify({"error": f"Falta {campo}"}), 400

        # Validaciones de negocio
        if data["equipo_local"] == data["equipo_visitante"]:
            return jsonify({"error": "Equipos iguales"}), 400

        fases_validas = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
        if data["fase"] not in fases_validas:
            return jsonify({"error": "Fase inválida"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # 409 → duplicado
        cursor.execute("""
            SELECT id FROM partidos 
            WHERE equipo_local=%s AND equipo_visitante=%s AND fecha=%s
        """, (data["equipo_local"], data["equipo_visitante"], data["fecha"]))

        if cursor.fetchone():
            return jsonify({"error": "El partido ya existe"}), 409

        # INSERT
        cursor.execute("""
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
            VALUES (%s, %s, %s, %s)
        """, (
            data["equipo_local"],
            data["equipo_visitante"],
            data["fecha"],
            data["fase"]
        ))

        conn.commit()

        return jsonify({
            "mensaje": "Partido creado",
            "id": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500