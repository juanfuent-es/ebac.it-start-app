"""Modelo Tarea (versión simple para principiantes).

Objetivo: centralizar CRUD con pocas funciones, devolver tipos básicos (tuplas y listas)
y añadir comentarios claros. Sin clases avanzadas ni decoradores.
"""

from database import execute, query_one, query_all
from .categoria import Categoria

class Tarea:
    """Operaciones básicas sobre la tabla `tareas`."""

    @staticmethod
    def validate(nombre, id_categoria_raw, fecha_limite=None, prioridad=None, tiempo_estimado=None):
        """Valida datos de entrada para Tarea y retorna (nombre_limpio, id_categoria, fecha_limite, prioridad, tiempo_estimado).

        Lanza ValueError con mensajes orientados al usuario si algo no es válido.
        """
        # Validación de nombre
        if nombre is None:
            raise ValueError("El nombre de la tarea es obligatorio")
        nombre = str(nombre).strip()
        if nombre == "":
            raise ValueError("El nombre de la tarea es obligatorio")

        # Validación de categoría
        if id_categoria_raw is None or str(id_categoria_raw).strip() == "":
            raise ValueError("Debes seleccionar una categoría válida")
        categoria_str = str(id_categoria_raw).strip()
        if categoria_str.isdigit():
            id_categoria = int(categoria_str)
            if not Categoria.get_by_id(id_categoria):
                raise ValueError("La categoría seleccionada no existe")
        else:
            row = Categoria.get_by_name(categoria_str)
            if not row:
                raise ValueError("La categoría seleccionada no existe")
            id_categoria = row["id"] if isinstance(row, dict) else row.id

        # Validación de fecha límite (opcional) - ahora acepta fecha y hora
        fecha_limite_ok = None
        if fecha_limite and str(fecha_limite).strip():
            fecha_limite_str = str(fecha_limite).strip()
            # Validar formato de fecha y hora (YYYY-MM-DDTHH:MM)
            try:
                from datetime import datetime
                # Intentar parsear el formato datetime-local
                if 'T' in fecha_limite_str:
                    datetime.strptime(fecha_limite_str, "%Y-%m-%dT%H:%M")
                else:
                    # Si solo tiene fecha, agregar hora por defecto (23:59)
                    datetime.strptime(fecha_limite_str, "%Y-%m-%d")
                    fecha_limite_str = fecha_limite_str + "T23:59"
                fecha_limite_ok = fecha_limite_str
            except ValueError:
                raise ValueError("La fecha límite debe tener el formato YYYY-MM-DD o YYYY-MM-DDTHH:MM")

        # Validación de prioridad
        prioridad_ok = "media"  # valor por defecto
        if prioridad and str(prioridad).strip():
            prioridad_valida = str(prioridad).strip().lower()
            if prioridad_valida in ["baja", "media", "alta"]:
                prioridad_ok = prioridad_valida
            else:
                raise ValueError("La prioridad debe ser: baja, media o alta")

        # Validación de tiempo estimado
        tiempo_estimado_ok = None
        if tiempo_estimado is not None and str(tiempo_estimado).strip():
            try:
                tiempo_estimado_ok = int(tiempo_estimado)
                if tiempo_estimado_ok < 0:
                    raise ValueError("El tiempo estimado no puede ser negativo")
            except ValueError:
                raise ValueError("El tiempo estimado debe ser un número entero válido")

        return nombre, id_categoria, fecha_limite_ok, prioridad_ok, tiempo_estimado_ok
    
    @staticmethod
    def create(nombre="", id_categoria=None, estado="pendiente", fecha_limite=None, prioridad=None, tiempo_estimado=None):
        """Valida datos, crea una tarea y devuelve su id (int).

        Reglas del esquema:
        - estado tiene default 'pendiente'
        - id_categoria es NOT NULL y debe existir
        - prioridad tiene default 'media'
        - fecha_creacion/fecha_actualizacion se gestionan en DB
        - completado_en se establece automáticamente cuando estado = 'completada'
        """
        # Validación centralizada
        nombre_ok, categoria_ok, fecha_limite_ok, prioridad_ok, tiempo_estimado_ok = Tarea.validate(
            nombre, id_categoria, fecha_limite, prioridad, tiempo_estimado
        )
        
        # Si el estado es completada, establecer completado_en
        completado_en = None
        if estado == "completada":
            completado_en = "datetime('now','localtime')"
        
        try:
            return execute(
                """INSERT INTO tareas (nombre, estado, id_categoria, fecha_limite, prioridad, tiempo_estimado, completado_en) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nombre_ok, estado, categoria_ok, fecha_limite_ok, prioridad_ok, tiempo_estimado_ok, completado_en),
            )
        except Exception as exc:
            # Normalizamos errores de integridad a ValueError con mensaje de usuario
            raise ValueError("No se pudo crear la tarea por una restricción de integridad.") from exc

    # ------------------------------------------------------------------
    # Leer (SELECT)
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_id(tarea_id):
        """Devuelve una fila con todos los campos de la tarea o None."""
        return query_one(
            """SELECT id, nombre, fecha_creacion, fecha_limite, prioridad, estado, tiempo_estimado, 
                      completado_en, id_categoria, fecha_actualizacion 
               FROM tareas WHERE id = ?""",
            (tarea_id,),
        )

    @staticmethod
    def get_all():
        """Devuelve lista de filas con todas las tareas."""
        return query_all(
            """SELECT id, nombre, fecha_creacion, fecha_limite, prioridad, estado, tiempo_estimado, 
                      completado_en, id_categoria, fecha_actualizacion 
               FROM tareas ORDER BY id"""
        )

    # ------------------------------------------------------------------
    # Actualizar (UPDATE) — funciones pequeñas y explícitas
    # ------------------------------------------------------------------
    @staticmethod
    def update(tarea_id, nuevo_nombre):
        """Cambia el nombre de la tarea y actualiza `fecha_actualizacion`."""
        execute(
            "UPDATE tareas SET nombre = ?, fecha_actualizacion = datetime('now','localtime') WHERE id = ?",
            (nuevo_nombre, tarea_id),
        )

    @staticmethod
    def set_estado(tarea_id, nuevo_estado):
        """Actualiza el estado (pendiente | en_progreso | completada) y `fecha_actualizacion`.
        
        Si el estado es 'completada', también establece completado_en.
        Si se cambia de 'completada' a otro estado, limpia completado_en.
        """
        if nuevo_estado == "completada":
            execute(
                """UPDATE tareas SET estado = ?, completado_en = datetime('now','localtime'), 
                   fecha_actualizacion = datetime('now','localtime') WHERE id = ?""",
                (nuevo_estado, tarea_id),
            )
        else:
            execute(
                """UPDATE tareas SET estado = ?, completado_en = NULL, 
                   fecha_actualizacion = datetime('now','localtime') WHERE id = ?""",
                (nuevo_estado, tarea_id),
            )

    @staticmethod
    def move_to_categoria(tarea_id, nueva_categoria_id):
        """Mueve la tarea a otra categoría (FK válida) y actualiza `fecha_actualizacion`."""
        execute(
            "UPDATE tareas SET id_categoria = ?, fecha_actualizacion = datetime('now','localtime') WHERE id = ?",
            (nueva_categoria_id, tarea_id),
        )

    @staticmethod
    def set_fecha_limite(tarea_id, fecha_limite):
        """Actualiza la fecha límite de la tarea y `fecha_actualizacion`."""
        execute(
            "UPDATE tareas SET fecha_limite = ?, fecha_actualizacion = datetime('now','localtime') WHERE id = ?",
            (fecha_limite, tarea_id),
        )

    @staticmethod
    def set_prioridad(tarea_id, prioridad):
        """Actualiza la prioridad de la tarea y `fecha_actualizacion`.
        
        Valores válidos: baja, media, alta
        """
        if prioridad not in ["baja", "media", "alta"]:
            raise ValueError("La prioridad debe ser: baja, media o alta")
        execute(
            "UPDATE tareas SET prioridad = ?, fecha_actualizacion = datetime('now','localtime') WHERE id = ?",
            (prioridad, tarea_id),
        )

    @staticmethod
    def set_tiempo_estimado(tarea_id, tiempo_estimado):
        """Actualiza el tiempo estimado de la tarea y `fecha_actualizacion`."""
        if tiempo_estimado is not None and tiempo_estimado < 0:
            raise ValueError("El tiempo estimado no puede ser negativo")
        execute(
            "UPDATE tareas SET tiempo_estimado = ?, fecha_actualizacion = datetime('now','localtime') WHERE id = ?",
            (tiempo_estimado, tarea_id),
        )

    # ------------------------------------------------------------------
    # Eliminar (DELETE)
    # ------------------------------------------------------------------
    @staticmethod
    def delete(tarea_id):
        """Elimina la tarea indicada."""
        execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))

    # ------------------------------------------------------------------
    # Consultas específicas con nuevos campos
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_prioridad(prioridad):
        """Devuelve lista de tareas filtradas por prioridad."""
        return query_all(
            """SELECT id, nombre, fecha_creacion, fecha_limite, prioridad, estado, tiempo_estimado, 
                      completado_en, id_categoria, fecha_actualizacion 
               FROM tareas WHERE prioridad = ? ORDER BY fecha_creacion DESC""",
            (prioridad,)
        )

    @staticmethod
    def get_tareas_vencidas():
        """Devuelve lista de tareas que han pasado su fecha límite y no están completadas."""
        return query_all(
            """SELECT id, nombre, fecha_creacion, fecha_limite, prioridad, estado, tiempo_estimado, 
                      completado_en, id_categoria, fecha_actualizacion 
               FROM tareas WHERE fecha_limite < datetime('now','localtime') 
               AND estado != 'completada' ORDER BY fecha_limite ASC"""
        )

    @staticmethod
    def get_tareas_completadas():
        """Devuelve lista de tareas completadas ordenadas por fecha de completado."""
        return query_all(
            """SELECT id, nombre, fecha_creacion, fecha_limite, prioridad, estado, tiempo_estimado, 
                      completado_en, id_categoria, fecha_actualizacion 
               FROM tareas WHERE estado = 'completada' ORDER BY completado_en DESC"""
        )

    @staticmethod
    def get_tiempo_total_estimado():
        """Devuelve la suma total del tiempo estimado de todas las tareas pendientes."""
        result = query_one(
            "SELECT SUM(tiempo_estimado) as total FROM tareas WHERE estado != 'completada' AND tiempo_estimado IS NOT NULL"
        )
        return result["total"] if result and result["total"] else 0

    # ------------------------------------------------------------------
    # JOINs — tareas con nombre de categoría
    # ------------------------------------------------------------------
    @staticmethod
    def with_categoria(categoria_id=None):
        """Delegado: usa Categoria.tareas_join para el JOIN tareas-categorías."""
        return Categoria.tareas_join(categoria_id)



