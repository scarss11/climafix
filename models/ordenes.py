from database import query

def get_all():
    return query("""
        SELECT o.*,
               c.nombre AS cliente_nombre,
               t.nombre AS tecnico_nombre,
               e.tipo   AS equipo_tipo,
               e.marca  AS equipo_marca
        FROM ordenes o
        LEFT JOIN clientes  c ON c.id=o.cliente_id
        LEFT JOIN tecnicos  t ON t.id=o.tecnico_id
        LEFT JOIN equipos   e ON e.id=o.equipo_id
        ORDER BY o.created_at DESC
    """, fetchall=True)

def get_by_id(oid):
    return query("""
        SELECT o.*,
               c.nombre AS cliente_nombre,
               t.nombre AS tecnico_nombre,
               e.tipo   AS equipo_tipo,
               e.marca  AS equipo_marca,
               e.modelo AS equipo_modelo
        FROM ordenes o
        LEFT JOIN clientes  c ON c.id=o.cliente_id
        LEFT JOIN tecnicos  t ON t.id=o.tecnico_id
        LEFT JOIN equipos   e ON e.id=o.equipo_id
        WHERE o.id=%s
    """, (oid,), fetchone=True)

def get_by_tecnico(tid):
    return query("""
        SELECT o.*,
               c.nombre AS cliente_nombre,
               e.tipo   AS equipo_tipo,
               e.marca  AS equipo_marca
        FROM ordenes o
        LEFT JOIN clientes c ON c.id=o.cliente_id
        LEFT JOIN equipos  e ON e.id=o.equipo_id
        WHERE o.tecnico_id=%s
        ORDER BY o.created_at DESC
    """, (tid,), fetchall=True)

def get_by_cliente(cid):
    return query("""
        SELECT o.*,
               t.nombre AS tecnico_nombre,
               e.tipo   AS equipo_tipo,
               e.marca  AS equipo_marca
        FROM ordenes o
        LEFT JOIN tecnicos t ON t.id=o.tecnico_id
        LEFT JOIN equipos  e ON e.id=o.equipo_id
        WHERE o.cliente_id=%s
        ORDER BY o.created_at DESC
    """, (cid,), fetchall=True)

def create(descripcion, cliente_id, tecnico_id, equipo_id):
    return query(
        "INSERT INTO ordenes (descripcion,cliente_id,tecnico_id,equipo_id) VALUES (%s,%s,%s,%s)",
        (descripcion, cliente_id, tecnico_id, equipo_id), commit=True
    )

def update_estado(oid, estado):
    return query("UPDATE ordenes SET estado=%s WHERE id=%s", (estado, oid), commit=True)

def update(oid, descripcion, estado, tecnico_id, equipo_id):
    return query(
        "UPDATE ordenes SET descripcion=%s,estado=%s,tecnico_id=%s,equipo_id=%s WHERE id=%s",
        (descripcion, estado, tecnico_id, equipo_id, oid), commit=True
    )

def delete(oid):
    return query("DELETE FROM ordenes WHERE id=%s", (oid,), commit=True)

def count_by_estado():
    rows = query("""
        SELECT estado, COUNT(*) AS total FROM ordenes GROUP BY estado
    """, fetchall=True)
    return {r['estado']: r['total'] for r in rows} if rows else {}
