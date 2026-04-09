-- ============================================================
-- BLOQUE 1: CREAR TABLAS
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin','tecnico','cliente')),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    usuario_id INT REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tecnicos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    usuario_id INT REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS equipos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(100),
    cliente_id INT REFERENCES clientes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ordenes (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(30) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente','en_proceso','completada','cancelada')),
    descripcion TEXT,
    cliente_id INT REFERENCES clientes(id),
    tecnico_id INT REFERENCES tecnicos(id),
    equipo_id INT REFERENCES equipos(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mantenimientos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('preventivo','correctivo')),
    descripcion TEXT,
    evidencia_url TEXT,
    fecha_ejecucion TIMESTAMP DEFAULT NOW(),
    orden_id INT REFERENCES ordenes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS repuestos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    costo NUMERIC(10,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS detalle_repuestos (
    id SERIAL PRIMARY KEY,
    mantenimiento_id INT REFERENCES mantenimientos(id) ON DELETE CASCADE,
    repuesto_id INT REFERENCES repuestos(id),
    cantidad INT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS cotizaciones (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    total NUMERIC(12,2) NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'borrador'
        CHECK (estado IN ('borrador','enviada','aprobada','rechazada')),
    notas TEXT,
    cliente_id INT REFERENCES clientes(id),
    orden_id INT REFERENCES ordenes(id)
);

-- ============================================================
-- BLOQUE 2: DATOS BASE — USUARIOS
-- ============================================================

INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Administrador','admin@climafix.com','HASH_PENDING','admin'),
('Carlos Técnico','carlos@climafix.com','HASH_PENDING','tecnico'),
('María López','maria@cliente.com','HASH_PENDING','cliente')
ON CONFLICT (email) DO NOTHING;

INSERT INTO clientes (nombre, telefono, direccion, usuario_id)
SELECT 'María López','3001234567','Calle 45 # 20-10, Bogotá', id
FROM usuarios WHERE email='maria@cliente.com'
ON CONFLICT DO NOTHING;

INSERT INTO tecnicos (nombre, especialidad, usuario_id)
SELECT 'Carlos Técnico','Sistemas VRF y Minisplit', id
FROM usuarios WHERE email='carlos@climafix.com'
ON CONFLICT DO NOTHING;

-- ============================================================
-- BLOQUE 3: DATOS DEMO
-- ============================================================

INSERT INTO repuestos (nombre, costo) VALUES
('Filtro HEPA','45000'),
('Gas R-410A (kg)','85000'),
('Capacitor arranque','35000'),
('Termostato digital','120000'),
('Sensor de temperatura','55000')
ON CONFLICT DO NOTHING;

INSERT INTO equipos (tipo, marca, modelo, numero_serie, cliente_id)
SELECT 'Minisplit','LG','Art Cool Premier 18000 BTU','LG-AC-2024-001', c.id
FROM clientes c WHERE c.nombre='María López'
ON CONFLICT DO NOTHING;

-- ============================================================
-- BLOQUE 4: ORDEN DEMO
-- ============================================================

INSERT INTO ordenes (descripcion, estado, cliente_id, tecnico_id, equipo_id)
SELECT
    'Mantenimiento preventivo trimestral',
    'pendiente',
    c.id,
    t.id,
    e.id
FROM clientes c
JOIN tecnicos t ON TRUE
JOIN equipos e ON e.cliente_id = c.id
WHERE c.nombre='María López'
LIMIT 1;
