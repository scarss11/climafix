from database import query

def get_by_orden(oid):
    return query("""
        SELECT m.*,
               COALESCE(
                   json_agg(
                       json_build_object('nombre', r.nombre, 'costo', r.costo, 'cantidad', dr.cantidad)
                   ) FILTER (WHERE r.id IS NOT NULL), '[]'
               ) AS repuestos
        FROM mantenimientos m
        LEFT JOIN detalle_repuestos dr ON dr.mantenimiento_id=m.id
        LEFT JOIN repuestos r ON r.id=dr.repuesto_id
        WHERE m.orden_id=%s
        GROUP BY m.id
        ORDER BY m.fecha_ejecucion DESC
    """, (oid,), fetchall=True)

def create(tipo, descripcion, evidencia_url, orden_id):
    return query(
        "INSERT INTO mantenimientos (tipo,descripcion,evidencia_url,orden_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (tipo, descripcion, evidencia_url, orden_id), fetchone=True
    )

def add_repuesto(mantenimiento_id, repuesto_id, cantidad):
    return query(
        "INSERT INTO detalle_repuestos (mantenimiento_id,repuesto_id,cantidad) VALUES (%s,%s,%s)",
        (mantenimiento_id, repuesto_id, cantidad), commit=True
    )
