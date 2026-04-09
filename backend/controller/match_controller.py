from backend.database.database import conectar_db

def mostrar_partidos(equipo, fecha, fase):
    conn = conectar_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM partidos WHERE 1=1" 
    params = []

    if fecha:
        sql += " AND fecha = %s"
        params.append(fecha)
    if equipo:
        sql += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.extend([equipo, equipo])
    if fase:
        sql += " AND fase = %s"
        params.append(fase)
    
    cursor.execute(sql, params)
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return partidos