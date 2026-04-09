from database import query

def get_all():
    return query("SELECT * FROM repuestos ORDER BY nombre", fetchall=True)

def create(nombre, costo):
    return query(
        "INSERT INTO repuestos (nombre,costo) VALUES (%s,%s)",
        (nombre, costo), commit=True
    )

def delete(rid):
    return query("DELETE FROM repuestos WHERE id=%s", (rid,), commit=True)
