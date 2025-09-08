"""Modelo Tarea (versión simple para principiantes).

Objetivo: centralizar CRUD con pocas funciones, devolver tipos básicos (tuplas y listas)
y añadir comentarios claros. Sin clases avanzadas ni decoradores.
"""

from database import execute, query_one, query_all
from .categoria import Categoria

class Tarea:
    """Operaciones básicas sobre la tabla `tareas`."""

    @staticmethod
    def validate(nombre, categoria_id_raw):
        """Valida datos de entrada para Tarea y retorna (nombre_limpio, categoria_id).

        Lanza ValueError con mensajes orientados al usuario si algo no es válido.
        """
        # Validación de nombre
        if nombre is None:
            raise ValueError("El nombre de la tarea es obligatorio")
        nombre = str(nombre).strip()
        if nombre == "":
            raise ValueError("El nombre de la tarea es obligatorio")

        # Validación de categoría
        if categoria_id_raw is None or str(categoria_id_raw).strip() == "":
            raise ValueError("Debes seleccionar una categoría válida")
        categoria_str = str(categoria_id_raw).strip()
        if categoria_str.isdigit():
            categoria_id = int(categoria_str)
            if not Categoria.get_by_id(categoria_id):
                raise ValueError("La categoría seleccionada no existe")
        else:
            row = Categoria.get_by_name(categoria_str)
            if not row:
                raise ValueError("La categoría seleccionada no existe")
            categoria_id = row["id"] if isinstance(row, dict) else row.id

        return nombre, categoria_id
    
    @staticmethod
    def create(nombre="", categoria_id=None, estado="pendiente"):
        """Valida datos, crea una tarea y devuelve su id (int).

        Reglas del esquema:
        - estado tiene default 'pendiente'
        - categoria_id es NOT NULL y debe existir
        - created_at/updated_at se gestionan en DB
        """
        # Validación centralizada
        nombre_ok, categoria_ok = Tarea.validate(nombre, categoria_id)
        try:
            return execute(
                "INSERT INTO tareas (nombre, estado, categoria_id) VALUES (?, ?, ?)",
                (nombre_ok, estado, categoria_ok),
            )
        except Exception as exc:
            # Normalizamos errores de integridad a ValueError con mensaje de usuario
            raise ValueError("No se pudo crear la tarea por una restricción de integridad.") from exc

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
            "SELECT id, nombre FROM tareas ORDER BY id"
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


