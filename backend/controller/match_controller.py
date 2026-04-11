from backend.database.database import consultar_db, conectar_db

def mostrar_partidos(equipo, fecha, fase, limit, offset):
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