import os
import sqlite3
from typing import Any, Iterable, Optional, Tuple, List


DB_PATH = os.path.join(os.path.dirname(__file__), "tareas.sqlite")


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute(sql: str, params: Iterable[Any] = ()) -> int:
    """Ejecuta INSERT/UPDATE/DELETE. Devuelve lastrowid para INSERT, o 0 en otros casos."""
    conn = _get_connection()
    try:
        cursor = conn.execute(sql, tuple(params))
        conn.commit()
        return cursor.lastrowid or 0
    finally:
        conn.close()


def query_one(sql: str, params: Iterable[Any] = ()) -> Optional[Tuple[Any, ...]]:
    """Ejecuta un SELECT y devuelve una sola fila (tupla) o None."""
    conn = _get_connection()
    try:
        cursor = conn.execute(sql, tuple(params))
        row = cursor.fetchone()
        return row
    finally:
        conn.close()


def query_all(sql: str, params: Iterable[Any] = ()) -> List[Tuple[Any, ...]]:
    """Ejecuta un SELECT y devuelve todas las filas como lista de tuplas."""
    conn = _get_connection()
    try:
        cursor = conn.execute(sql, tuple(params))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def init_db() -> None:
    """Crea tablas si no existen y datos mínimos (categoría General)."""
    conn = _get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT (datetime('now','localtime')),
                updated_at TEXT DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente',
                categoria_id INTEGER NOT NULL,
                created_at TEXT DEFAULT (datetime('now','localtime')),
                updated_at TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT ON UPDATE CASCADE
            );
            """
        )

        # Asegurar categoría por defecto
        cur = conn.execute("SELECT id FROM categorias WHERE nombre = ?", ("General",))
        row = cur.fetchone()
        if row is None:
            conn.execute("INSERT INTO categorias (nombre) VALUES (?)", ("General",))
        conn.commit()
    finally:
        conn.close()


# Inicializa base al importar el módulo
init_db()

