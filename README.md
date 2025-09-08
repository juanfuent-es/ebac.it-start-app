# Rutina.py

**Rutina.py** es un gestor de tareas desarrollado como proyecto guía del curso **IT Start**.  
El repositorio concentra la evolución del proyecto desde un backend básico en Flask hasta la integración con SQLite, APIs y análisis de datos.

## Módulos cubiertos
- **Módulo 6 – Backend con Flask**  
  Rutas y manejo de tareas en memoria.
- **Módulo 7 – Gestión de información con SQLite**  
  Persistencia de datos en base relacional.
- **Módulo 8 – Fullstack con APIs**  
  Comunicación Frontend–Backend y manejo de errores.
- **Módulo 9 – Ciencia de Datos**  
  Exploración y visualización de datos con Pandas.

## Uso básico
Clona el repositorio y ejecuta la aplicación localmente:

```bash
git clone https://github.com/juanfuent-es/ebac.it-start-app.git
cd ebac.it-start-app
pip install -r requirements.txt
flask run

## Estructura por temas (Guía)

1. Prepara tus rutas y conecta tu base de datos
   - Inicialización en `database.py` con `init_db()` y helpers `execute/query_*`.
   - En `app.py` se importa e invoca `init_db()` al inicio.

2. Esquematiza tus rutas CRUD
   - `GET /tareas` listar
   - `GET|POST /crear` crear
   - `GET /detalle-tarea/<indice>` detalle
   - `GET|POST /editar-tarea/<indice>` editar/actualizar
   - `GET /eliminar/<indice>` eliminar
   - `GET /filtrar-tareas/<filtro>` filtro por nombre

3. Prepara tus vistas HTML y estructura de carpetas
   - Vistas en `templates/` con `layout.html` como base.
   - `tareas.html`, `formulario.html`, `editar_tarea.html`, `detalle_tarea.html`.

4. Crea una nueva tarea desde un formulario web
   - Formulario en `formulario.html` (campo `title`).
   - Controlador en `app.py` (`/crear` POST) crea tarea con categoría por defecto.

5. Listar todas las tareas registradas
   - `Tarea.get_all()` y render en `tareas.html`.

6. Consulta el detalle de una tarea específica
   - `GET /detalle-tarea/<indice>` mapea índice UI → id y usa `Tarea.get_by_id`.

7. Edita una tarea existente / 8. Actualiza una tarea existente
   - `GET /editar-tarea/<indice>` muestra `editar_tarea.html`.
   - `POST /editar-tarea/<indice>` actualiza con `Tarea.update`.

9. Elimina una tarea desde la interfaz
   - `GET /eliminar/<indice>` elimina con `Tarea.delete`.

10. Conclusión y recursos adicionales
   - Consulta Flask (`https://flask.palletsprojects.com/`), Jinja (`https://jinja.palletsprojects.com/`) y SQLite (`https://www.sqlite.org/docs.html`).
   - El flujo se basa en rutas simples y helpers de DB, con plantillas Bootstrap.