# database.py
import sqlite3

DATABASE_NAME = "tareas.sqlite"

def connect_db():
    """
    Conecta a la base de datos
    """
    conn = sqlite3.connect(DATABASE_NAME) # Conecta a la base de datos
    conn.execute("PRAGMA foreign_keys = ON") # Activa el modo de clave foránea
    print(" * Conectado a la base de datos")
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
    return conn

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
        - estado (TEXT NOT NULL): Estado de la tarea (pendiente, en progreso, completada)
        - categoria_id (INTEGER): Identificador de la categoría de la tarea (opcional)
        - created_at (DATE): Fecha de creación de la tarea
        - updated_at (DATE): Fecha de actualización de la tarea
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            categoria_id INTEGER NOT NULL,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE,
            updated_at DATE NOT NULL DEFAULT CURRENT_DATE,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
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
        ON tareas(categoria_id, estado);
    """)
    conn.commit()
    print(" * Índice idx_tareas_categoria_estado creado")
