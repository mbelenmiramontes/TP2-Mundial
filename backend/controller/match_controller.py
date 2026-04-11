from backend.database.database import conectar_db

def mostrar_partidos(equipo, fecha, fase, limit, offset):
    conn = conectar_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM partidos"
    condition = " WHERE 1=1" 
    pagination = " "
    params = []

    if fecha:
        condition += " AND fecha = %s"
        params.append(fecha)
    if equipo:
        condition += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.extend([equipo, equipo])
    if fase:
        condition += " AND fase = %s"
        params.append(fase)
    
    cursor.execute("SELECT COUNT(*) as total FROM partidos " + condition, params)
    total = cursor.fetchone()
    
    if limit:
        pagination += " LIMIT %s"
        params.append(limit)
    if offset is not None:
        pagination += " OFFSET %s"
        params.append(offset)
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql + condition + pagination, params)
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return partidos, total
