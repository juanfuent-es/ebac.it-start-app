# database.py
import sqlite3
import os

if os.environ.get('ENVIRONMENT') == 'production':
    DATABASE_NAME = 'tareas_prod.sqlite'
else:
    DATABASE_NAME = 'tareas_dev.sqlite'

def connect_db():
    """
    Conecta a la base de datos
    """
    conn = sqlite3.connect(DATABASE_NAME) # Conecta a la base de datos
    conn.row_factory = sqlite3.Row  # Devuelve filas tipo Row: acceso por índice y por llave
    conn.execute("PRAGMA foreign_keys = ON") # Activa el modo de clave foránea
    print(f" * Conectado a: {DATABASE_NAME}")
    return conn

# Función para inicializar la base 
def init_db():
    """
    Inicializa la base de datos
    En este método se define la estructura de la base de datos
    creando tablas, índices, etc.
    """
    conn = connect_db()
    print(" * Inicializando base de datos")
    create_table_categorias(conn)
    create_table_tareas(conn)
    create_indices(conn)
    conn.close()


def create_table_categorias(conn):
    """
    Tabla: categorias
    Columnas:
        - id (INTEGER PRIMARY KEY AUTOINCREMENT): Identificador único de la categoría
        - nombre (TEXT NOT NULL UNIQUE): Nombre de la categoría (no puede repetirse)
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    print(" * Tabla categorias creada")

def create_table_tareas(conn):
    """
    Tabla: tareas
    
    Columnas:
        - id (INTEGER PRIMARY KEY AUTOINCREMENT): Identificador único de la tarea
        - nombre (TEXT NOT NULL): Nombre de la tarea
        - fecha_creacion (TEXT): Fecha y hora de creación de la tarea
        - fecha_limite (TEXT): Fecha y hora límite para completar la tarea (formato: YYYY-MM-DDTHH:MM)
        - prioridad (TEXT): Prioridad de la tarea (baja, media, alta)
        - estado (TEXT NOT NULL): Estado de la tarea (pendiente, en progreso, completada)
        - tiempo_estimado (INTEGER): Tiempo estimado en minutos
        - completado_en (TEXT): Fecha y hora de completado de la tarea (null si no se ha completado)
        - id_categoria (INTEGER): Identificador de la categoría de la tarea
        - fecha_actualizacion (TEXT): Fecha y hora de actualización de la tarea
        
    NOTA: fecha_limite ahora maneja fecha y hora en formato ISO (YYYY-MM-DDTHH:MM)
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            fecha_limite TEXT,
            prioridad TEXT DEFAULT 'media',
            estado TEXT NOT NULL DEFAULT 'pendiente',
            tiempo_estimado INTEGER,
            completado_en TEXT,
            id_categoria INTEGER NOT NULL,
            fecha_actualizacion TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (id_categoria) REFERENCES categorias(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );
    """)
    conn.commit()
    print(" * Tabla tareas creada")

def create_indices(conn):
    """
    Índices recomendados según consultas más comunes:
      - Buscar tareas por categoría y estado
    """
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_tareas_categoria_estado
        ON tareas(id_categoria, estado);
    """)
    conn.commit()
    print(" * Índice idx_tareas_categoria_estado creado")

# -----------------------------------------------------------------------------
# Helpers simples: ejecutar consultas sin repetir conexión
# C - CREATE -> INSERT
# R - READ -> SELECT
# U - UPDATE -> UPDATE
# D - DELETE -> DELETE
# -----------------------------------------------------------------------------
def execute(sql, params=None):
    """
    Ejecuta INSERT/UPDATE/DELETE. Devuelve lastrowid si aplica, o None.
    """
    conn = connect_db()
    cur = conn.execute(sql, params or ())
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def query_all(sql, params=None):
    """Ejecuta SELECT y devuelve lista de filas."""
    conn = connect_db()
    rows = conn.execute(sql, params or ()).fetchall()
    conn.close()
    return rows

def query_one(sql, params=None):
    """Ejecuta SELECT y devuelve una fila o None."""
    conn = connect_db()
    row = conn.execute(sql, params or ()).fetchone()
    conn.close()
    return row
