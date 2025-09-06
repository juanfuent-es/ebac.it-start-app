"""Modelo Categoria (versión simple para principiantes).

Devuelve tipos básicos (id y filas) y usa solo métodos estáticos.
"""

from database import execute, query_one, query_all

""" CRUD
- C - CREATE -> INSERT
- R - READ -> SELECT
- U - UPDATE -> UPDATE
- D - DELETE -> DELETE
"""

class Categoria:
    """Operaciones básicas sobre la tabla `categorias`."""

    @staticmethod
    def create(nombre):
        """Crea una categoría y devuelve su id (int)."""
        return execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))

    @staticmethod
    def get_by_id(categoria_id):
        """Devuelve una fila (id, nombre) o None."""
        return query_one(
            "SELECT id, nombre FROM categorias WHERE id = ?",
            (categoria_id,),
        )

    @staticmethod
    def get_all():
        """Devuelve una lista de filas (id, nombre)."""
        return query_all("SELECT id, nombre FROM categorias ORDER BY id")

    @staticmethod
    def update(categoria_id, nuevo_nombre):
        """Cambia el nombre de la categoría indicada."""
        execute(
            "UPDATE categorias SET nombre = ? WHERE id = ?",
            (nuevo_nombre, categoria_id),
        )

    @staticmethod
    def delete(categoria_id):
        """Elimina la categoría indicada (si no hay tareas vinculadas)."""
        execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))