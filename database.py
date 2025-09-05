import sqlite3
print(" * Inicializando base de datos")

def get_connection():
    conn = sqlite3.connect("tareas.db")
    return conn

# Función para inicializar la base 
def init_db():
    conn = get_connection()
    # En este método se define la estructura de la base de datos
    # creando tablas, índices, etc.
    print(" * Base de datos conectada")