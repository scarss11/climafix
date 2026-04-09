from database import query

def get_all():
    return query("""
        SELECT cl.*, u.email FROM clientes cl
        LEFT JOIN usuarios u ON u.id=cl.usuario_id
        ORDER BY cl.nombre
    """, fetchall=True)

def get_by_id(cid):
    return query("SELECT * FROM clientes WHERE id=%s", (cid,), fetchone=True)

def get_by_usuario(uid):
    return query("SELECT * FROM clientes WHERE usuario_id=%s", (uid,), fetchone=True)

def create(nombre, telefono, direccion, usuario_id=None):
    return query(
        "INSERT INTO clientes (nombre,telefono,direccion,usuario_id) VALUES (%s,%s,%s,%s)",
        (nombre, telefono, direccion, usuario_id), commit=True
    )

def update(cid, nombre, telefono, direccion):
    return query(
        "UPDATE clientes SET nombre=%s,telefono=%s,direccion=%s WHERE id=%s",
        (nombre, telefono, direccion, cid), commit=True
    )

def delete(cid):
    return query("DELETE FROM clientes WHERE id=%s", (cid,), commit=True)
