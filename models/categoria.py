from database import execute, query_one, query_all

class Categoria:
    """Operaciones básicas sobre la tabla `categorias`."""
    # ------------------------------------------------------------------
    # Crear
    # ------------------------------------------------------------------
    @staticmethod
    def create(nombre):
        """Crea una categoría y devuelve su id (int)."""
        query = execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        print(f" * Categoría creada: {query}")
        return query

    # ------------------------------------------------------------------
    # Leer (SELECT)
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_id(categoria_id):
        """Devuelve una fila (id, nombre) o None."""
        query = query_one("SELECT id, nombre FROM categorias WHERE id = ?", (categoria_id,))
        print(f" * Categoría: {query}")
        return query

    @staticmethod
    def get_all():
        """Devuelve lista de filas con todas las categorías."""
        query = query_all("SELECT id, nombre FROM categorias ORDER BY id")
        print(f" * Categorías: {query}")
        return query

    @staticmethod
    def get_by_nombre(nombre):
        """Devuelve una fila (id, nombre) cuyo nombre coincide exactamente, o None."""
        query = query_one("SELECT id, nombre FROM categorias WHERE lower(nombre) = lower(?)", (nombre,))
        print(f" * Categoría por nombre '{nombre}': {query}")
        return query

    # ------------------------------------------------------------------
    # Actualizar (UPDATE)
    # ------------------------------------------------------------------
    @staticmethod
    def update(categoria_id, nuevo_nombre):
        """Actualiza el nombre de la categoría."""
        query = execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nuevo_nombre, categoria_id))
        print(f" * Nombre de categoría actualizada a: {nuevo_nombre}")
        return query

    # ------------------------------------------------------------------
    # Eliminar (DELETE)
    # ------------------------------------------------------------------
    @staticmethod
    def delete(categoria_id):
        """Elimina la categoría indicada."""
        query = execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        print(f" * Categoría eliminada: {query}")
        return query
