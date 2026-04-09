from database import query

def get_all():
    return query("""
        SELECT t.*, u.email FROM tecnicos t
        LEFT JOIN usuarios u ON u.id=t.usuario_id
        ORDER BY t.nombre
    """, fetchall=True)

def get_by_id(tid):
    return query("SELECT * FROM tecnicos WHERE id=%s", (tid,), fetchone=True)

def get_by_usuario(uid):
    return query("SELECT * FROM tecnicos WHERE usuario_id=%s", (uid,), fetchone=True)

def create(nombre, especialidad, usuario_id=None):
    return query(
        "INSERT INTO tecnicos (nombre,especialidad,usuario_id) VALUES (%s,%s,%s)",
        (nombre, especialidad, usuario_id), commit=True
    )

def update(tid, nombre, especialidad):
    return query(
        "UPDATE tecnicos SET nombre=%s,especialidad=%s WHERE id=%s",
        (nombre, especialidad, tid), commit=True
    )

def delete(tid):
    return query("DELETE FROM tecnicos WHERE id=%s", (tid,), commit=True)
