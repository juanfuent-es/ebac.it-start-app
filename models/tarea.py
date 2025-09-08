"""Modelo Tarea (versión simple para principiantes).

Objetivo: centralizar CRUD con pocas funciones, devolver tipos básicos (tuplas y listas)
y añadir comentarios claros. Sin clases avanzadas ni decoradores.
"""

from database import execute, query_one, query_all
from .categoria import Categoria

class Tarea:
    """Operaciones básicas sobre la tabla `tareas`."""
    @staticmethod
    def create(nombre, categoria_id, estado="pendiente"):
        """Crea una tarea y devuelve su id (int).

        Reglas del esquema:
        - estado tiene default 'pendiente' (puedes omitirlo si quieres usar ese valor)
        - categoria_id es NOT NULL (siempre debe existir la categoría)
        - created_at/updated_at se rellenan automát. con la fecha actual
        """
        return execute(
            "INSERT INTO tareas (nombre, estado, categoria_id) VALUES (?, ?, ?)",
            (nombre, estado, categoria_id),
        )

    # ------------------------------------------------------------------
    # Leer (SELECT)
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_id(tarea_id):
        """Devuelve una fila (id, nombre, estado, categoria_id, created_at, updated_at) o None."""
        return query_one(
            "SELECT id, nombre, estado, categoria_id, created_at, updated_at FROM tareas WHERE id = ?",
            (tarea_id,),
        )

    @staticmethod
    def get_all():
        """Devuelve lista de filas con todas las tareas."""
        return query_all(
            "SELECT id, nombre, estado, categoria_id, created_at, updated_at FROM tareas ORDER BY id"
        )

    # ------------------------------------------------------------------
    # Actualizar (UPDATE) — funciones pequeñas y explícitas
    # ------------------------------------------------------------------
    @staticmethod
    def update(tarea_id, nuevo_nombre):
        """Cambia el nombre de la tarea y actualiza `updated_at`."""
        execute(
            "UPDATE tareas SET nombre = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (nuevo_nombre, tarea_id),
        )

    @staticmethod
    def set_estado(tarea_id, nuevo_estado):
        """Actualiza el estado (pendiente | completada) y `updated_at`."""
        execute(
            "UPDATE tareas SET estado = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (nuevo_estado, tarea_id),
        )

    @staticmethod
    def move_to_categoria(tarea_id, nueva_categoria_id):
        """Mueve la tarea a otra categoría (FK válida) y actualiza `updated_at`."""
        execute(
            "UPDATE tareas SET categoria_id = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (nueva_categoria_id, tarea_id),
        )

    # ------------------------------------------------------------------
    # Eliminar (DELETE)
    # ------------------------------------------------------------------
    @staticmethod
    def delete(tarea_id):
        """Elimina la tarea indicada."""
        execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))

    # ------------------------------------------------------------------
    # JOINs — tareas con nombre de categoría
    # ------------------------------------------------------------------
    @staticmethod
    def with_categoria(categoria_id=None):
        """Delegado: usa Categoria.tareas_join para el JOIN tareas-categorías."""
        return Categoria.tareas_join(categoria_id)


