from database import query

def get_all():
    return query("""
        SELECT e.*, c.nombre AS cliente_nombre FROM equipos e
        LEFT JOIN clientes c ON c.id=e.cliente_id
        ORDER BY e.id DESC
    """, fetchall=True)

def get_by_id(eid):
    return query("SELECT * FROM equipos WHERE id=%s", (eid,), fetchone=True)

def get_by_cliente(cid):
    return query("SELECT * FROM equipos WHERE cliente_id=%s ORDER BY id DESC", (cid,), fetchall=True)

def create(tipo, marca, modelo, numero_serie, cliente_id):
    return query(
        "INSERT INTO equipos (tipo,marca,modelo,numero_serie,cliente_id) VALUES (%s,%s,%s,%s,%s)",
        (tipo, marca, modelo, numero_serie, cliente_id), commit=True
    )

def update(eid, tipo, marca, modelo, numero_serie):
    return query(
        "UPDATE equipos SET tipo=%s,marca=%s,modelo=%s,numero_serie=%s WHERE id=%s",
        (tipo, marca, modelo, numero_serie, eid), commit=True
    )

def delete(eid):
    return query("DELETE FROM equipos WHERE id=%s", (eid,), commit=True)
