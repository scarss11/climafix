from database import query

def get_all():
    return query("""
        SELECT cot.*, c.nombre AS cliente_nombre FROM cotizaciones cot
        LEFT JOIN clientes c ON c.id=cot.cliente_id
        ORDER BY cot.fecha DESC
    """, fetchall=True)

def get_by_id(cid):
    return query("""
        SELECT cot.*, c.nombre AS cliente_nombre FROM cotizaciones cot
        LEFT JOIN clientes c ON c.id=cot.cliente_id
        WHERE cot.id=%s
    """, (cid,), fetchone=True)

def get_by_cliente(cid):
    return query("""
        SELECT * FROM cotizaciones WHERE cliente_id=%s ORDER BY fecha DESC
    """, (cid,), fetchall=True)

def create(total, notas, cliente_id, orden_id=None):
    return query(
        "INSERT INTO cotizaciones (total,notas,cliente_id,orden_id) VALUES (%s,%s,%s,%s)",
        (total, notas, cliente_id, orden_id), commit=True
    )

def update_estado(cid, estado):
    return query("UPDATE cotizaciones SET estado=%s WHERE id=%s", (estado, cid), commit=True)

def delete(cid):
    return query("DELETE FROM cotizaciones WHERE id=%s", (cid,), commit=True)
