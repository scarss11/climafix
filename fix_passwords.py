"""
Ejecutar una sola vez después de crear las tablas:
  python fix_passwords.py
"""
from werkzeug.security import generate_password_hash
from database import query

USUARIOS = [
    ('admin@climafix.com',  'Admin2025!'),
    ('carlos@climafix.com', 'Tecnico2025!'),
    ('maria@cliente.com',   'Cliente2025!'),
]

for email, pw in USUARIOS:
    hashed = generate_password_hash(pw)
    ok = query("UPDATE usuarios SET password=%s WHERE email=%s", (hashed, email), commit=True)
    print(f"{'✓' if ok else '✗'} {email}")

print("\nPasswords actualizados correctamente.")
