# database.py
import sqlite3
print(" * Inicializando base de datos")

def get_connection():
    """
    Abre/conecta a tareas.db y habilita integridad referencial.
    Activar foreign_keys en cada conexión evita referencias inválidas.
    """
    conn = sqlite3.connect("tareas.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Función para inicializar la base 
def init_db():
    conn = get_connection()
    # En este método se define la estructura de la base de datos
    # creando tablas, índices, etc.
    try:
        create_table_categorias(conn)
        print(" * Tabla categorias creada")
        create_table_tareas(conn)
        print(" * Tabla tareas creada")
        create_indices(conn)  # opcional: acelera consultas comunes
        print(" * Índices creados")
        conn.commit()
    finally:
        conn.close()
    print(" * Base de datos conectada")

def create_table_categorias(conn):
    """
    Tabla: categorias
      - id (INTEGER, PK AUTOINCREMENT)
      - nombre (TEXT, NOT NULL, UNIQUE)
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
    """)

def create_table_tareas(conn):
    """
    Tabla: tareas
      - id (INTEGER, PK AUTOINCREMENT)
      - nombre (TEXT, NOT NULL)
      - categoria_id (INTEGER, NOT NULL) -> FK a categorias(id)
      - estado (TEXT, NOT NULL)  # 'pendiente', 'completada', etc.
      - created_at (TEXT, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
      - updated_at (TEXT, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            estado TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );
    """)

def create_indices(conn):
    """
    Índices recomendados según consultas más comunes:
      - Buscar tareas por categoría y estado
    """
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_tareas_categoria_estado
        ON tareas(categoria_id, estado);
    """)
