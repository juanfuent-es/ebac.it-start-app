from database import execute, query_one, query_all

class Categoria:
    """Operaciones básicas sobre la tabla `categorias`."""
    # ------------------------------------------------------------------
    # Crear
    # ------------------------------------------------------------------
    @staticmethod
    def create(nombre):
        """Crea una categoría y devuelve su id (int)."""
        if nombre == "":
            raise ValueError("El nombre de la categoría es obligatorio")
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
    def get_by_name(nombre):
        """Devuelve una fila (id, nombre) o None."""
        return query_one("SELECT id, nombre FROM categorias WHERE nombre = ?", (nombre,))

    @staticmethod
    def get_or_create(nombre):
        """Devuelve un id; crea la categoría si no existe. Limpia y valida nombre."""
        if nombre == "":
            raise ValueError("El nombre de la categoría es obligatorio")
        row = Categoria.get_by_name(nombre)
        if not row:
            return Categoria.create(nombre)
        return row["id"]

    @staticmethod
    def get_all():
        """Devuelve lista de filas con todas las categorías."""
        query = query_all("SELECT id, nombre FROM categorias ORDER BY id")
        print(f" * Categorías: {query}")
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

    # ------------------------------------------------------------------
    # JOINs — tareas con nombre de categoría
    # ------------------------------------------------------------------
    @staticmethod
    def tareas_join(categoria_id=None):
        """Devuelve tareas con el nombre de la categoría incluido.
        
        Si categoria_id es None, devuelve todas las tareas con sus categorías.
        Si categoria_id es especificado, filtra por esa categoría.
        """
        if categoria_id is None:
            return query_all(
                """SELECT t.id, t.nombre, t.creado_en, t.fecha_limite, t.prioridad, t.estado, 
                          t.tiempo_estimado, t.completado_en, t.id_categoria, t.actualizado_en,
                          c.nombre as categoria_nombre
                   FROM tareas t 
                   LEFT JOIN categorias c ON t.id_categoria = c.id 
                   ORDER BY t.id"""
            )
        else:
            return query_all(
                """SELECT t.id, t.nombre, t.creado_en, t.fecha_limite, t.prioridad, t.estado, 
                          t.tiempo_estimado, t.completado_en, t.id_categoria, t.actualizado_en,
                          c.nombre as categoria_nombre
                   FROM tareas t 
                   LEFT JOIN categorias c ON t.id_categoria = c.id 
                   WHERE t.id_categoria = ?
                   ORDER BY t.id""",
                (categoria_id,)
            )