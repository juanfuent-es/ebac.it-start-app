from database import execute, query_one, query_all


class Categoria:
    """Operaciones básicas sobre la tabla `categorias`. Devuelve tuplas/listas.

    Columnas: id, nombre, created_at, updated_at
    """

    @staticmethod
    def create(nombre: str) -> int:
        return execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))

    @staticmethod
    def get_by_id(categoria_id: int):
        return query_one(
            "SELECT id, nombre, created_at, updated_at FROM categorias WHERE id = ?",
            (categoria_id,),
        )

    @staticmethod
    def get_all():
        return query_all(
            "SELECT id, nombre, created_at, updated_at FROM categorias ORDER BY nombre"
        )

    @staticmethod
    def update(categoria_id: int, nuevo_nombre: str) -> None:
        execute(
            "UPDATE categorias SET nombre = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (nuevo_nombre, categoria_id),
        )

    @staticmethod
    def delete(categoria_id: int) -> None:
        execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))

    # JOIN auxiliar para tareas
    @staticmethod
    def tareas_join(categoria_id: int | None = None):
        sql = (
            "SELECT t.id, t.nombre, t.estado, t.categoria_id, c.nombre as categoria, t.created_at, t.updated_at "
            "FROM tareas t JOIN categorias c ON t.categoria_id = c.id "
        )
        params = ()
        if categoria_id is not None:
            sql += "WHERE c.id = ? "
            params = (categoria_id,)
        sql += "ORDER BY t.id"
        return query_all(sql, params)

