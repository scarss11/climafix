from database import query
from werkzeug.security import generate_password_hash, check_password_hash

def get_by_email(email):
    return query("SELECT * FROM usuarios WHERE email=%s", (email,), fetchone=True)

def get_by_id(uid):
    return query("SELECT * FROM usuarios WHERE id=%s", (uid,), fetchone=True)

def get_all():
    return query("SELECT * FROM usuarios ORDER BY nombre", fetchall=True)

def create(nombre, email, password, rol):
    hashed = generate_password_hash(password)
    return query(
        "INSERT INTO usuarios (nombre,email,password,rol) VALUES (%s,%s,%s,%s)",
        (nombre, email, hashed, rol), commit=True
    )

def update(uid, nombre, email, rol):
    return query(
        "UPDATE usuarios SET nombre=%s, email=%s, rol=%s WHERE id=%s",
        (nombre, email, rol, uid), commit=True
    )

def delete(uid):
    return query("DELETE FROM usuarios WHERE id=%s", (uid,), commit=True)

def verify_password(user, password):
    return check_password_hash(user['password'], password)
