# =============================================================================
# APLICACIÓN WEB FLASK - GESTOR DE TAREAS
# =============================================================================
# Este archivo contiene la lógica principal de nuestra aplicación web
# Flask es un framework web ligero para Python que nos permite crear
# aplicaciones web de forma sencilla

# PREPARA TUS RUTAS Y CONECTA TU BASE DE DATOS
# --------------------------------------------
# En esta sección importamos dependencias, inicializamos la base
# de datos y declaramos utilidades de apoyo.
# Importamos las clases y funciones que necesitamos de Flask
from flask import Flask, render_template, request, redirect
from database import init_db
from models.categoria import Categoria
from models.tarea import Tarea
# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial de Python que contiene el nombre del módulo
app = Flask(__name__)
init_db()

# -----------------------------------------------------------------------------
# Utilidad: resolver y validar categoría (por id o por nombre)
# -----------------------------------------------------------------------------
def _resolver_categoria_id(valor_categoria):
    """
    Dado un valor enviado desde el formulario en el campo "categoria",
    intenta resolver el id de la categoría:
      - Si es un número válido, verifica que exista por id
      - Si no es número, busca por nombre (case-insensitive)

    Devuelve el id (int) si existe o None si no se encontró.
    """
    if not valor_categoria:
        return None
    # Intentar tratarlo como id numérico
    try:
        posible_id = int(valor_categoria)
        fila = Categoria.get_by_id(posible_id)
        return fila["id"] if fila else None
    except (ValueError, TypeError):
        pass
    # Buscar por nombre exacto (insensible a mayúsculas)
    fila = Categoria.get_by_nombre(valor_categoria)
    return fila["id"] if fila else None

# =============================================================================
# ESQUEMATIZA TUS RUTAS CRUD - Crear, Leer, Actualizar, Eliminar
# =============================================================================
# Las rutas son las URLs que los usuarios pueden visitar en nuestro sitio web.
# Esquema general del CRUD:
#   - GET  /                        -> Listar todas las tareas registradas
#   - GET  /crear                   -> Formulario: crear nueva tarea
#   - POST /crear                   -> Crear una nueva tarea desde formulario web
#   - GET  /tarea/<id>          -> Consulta el detalle de una tarea específica
#   - GET  /editar/<id>         -> Edita una tarea existente (vista)
#   - POST /editar/<id>         -> Actualiza una tarea existente
#   - GET  /eliminar/<id>       -> Elimina una tarea desde la interfaz
#   - GET  /filtrar/<filtro>        -> Listado filtrado por categoría o estado
#   - GET  /acerca                  -> Página "Acerca de"

@app.route("/")
def index():
    """
    HOME - Muestra todas las tareas guardadas en la base de datos.
    """
    registros = Tarea.get_all()
    return render_template("index.html", tareas=registros)

@app.route("/crear", methods=["GET", "POST"])
def nueva_tarea():
    """
    CREA UNA NUEVA TAREA DESDE UN FORMULARIO WEB
    --------------------------------------------
    Ruta para crear nuevas tareas.
    - GET: Muestra el formulario para crear una tarea
    - POST: Procesa los datos del formulario y guarda la tarea
    """
    # Verificamos si la petición es POST (envío de formulario)
    if request.method == "POST":
        # Obtenemos el título de la tarea desde el formulario
        nombre = request.form["title"]
        valor_categoria = request.form.get("categoria")
        categoria_id = _resolver_categoria_id(valor_categoria)
        if categoria_id is None:
            # Si no existe la categoría, regresamos al formulario
            categorias = Categoria.get_all()
            error = "La categoría indicada no existe. Selecciona una válida."
            return render_template("formulario.html", categorias=categorias, error=error, nombre=nombre, categoria_input=valor_categoria)
        Tarea.create(nombre=nombre, categoria_id=categoria_id)
        return redirect("/")
    else:
        # Si la petición es GET, mostramos el formulario con categorías existentes
        categorias = Categoria.get_all()  # [(id, nombre), ...]
        return render_template("formulario.html", categorias=categorias)

@app.route('/tarea/<int:id>')
def detalle(id):
    """
    CONSULTA EL DETALLE DE UNA TAREA ESPECÍFICA
    """
    tarea = Tarea.get_by_id(id)
    categoria = Categoria.get_by_id(tarea["categoria_id"])
    return render_template("tarea.html", tarea=tarea, categoria=categoria)

@app.route('/tarea/<int:id>/toggle-estado', methods=["POST"])
def toggle_estado(id):
    """
    Alterna el estado de la tarea entre 'pendiente' y 'completada'.
    """
    tarea = Tarea.get_by_id(id)
    if not tarea:
        return redirect("/")
    nuevo_estado = "pendiente" if tarea["estado"] == "completada" else "completada"
    Tarea.set_estado(id, nuevo_estado)
    return redirect(f"/tarea/{id}")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """
    EDITA Y ACTUALIZA UNA TAREA EXISTENTE
    -------------------------------------
    Ruta para editar una tarea específica
    - <int:id>: Convierte el parámetro de la URL en un número entero
    - GET: Muestra el formulario con la tarea actual
    - POST: Guarda los cambios de la tarea
    """
    tarea = Tarea.get_by_id(id)
    if request.method == "POST":
        nuevo_nombre = request.form["title"]
        nueva_categoria_id = request.form.get("categoria")
        # Actualizamos nombre si cambió
        Tarea.update(id, nuevo_nombre)
        # Movemos de categoría si cambió
        if nueva_categoria_id != tarea["categoria_id"]:
            Tarea.move_to_categoria(id, nueva_categoria_id)
        return redirect(f"/tarea/{id}")
    else:
        # Pasamos datos necesarios: nombre, índice, categorías y categoría actual
        categorias = Categoria.get_all()
        return render_template(
            "editar.html",
            tarea=tarea,
            categorias=categorias
        )

@app.route("/eliminar/<int:id>")
def eliminar(id):
    """
    ELIMINA UNA TAREA DESDE LA INTERFAZ
    -----------------------------------
    Ruta para eliminar una tarea específica
    Elimina la tarea del índice especificado y redirige a la lista
    """
    tarea = Tarea.get_by_id(id)
    if tarea:
        Tarea.delete(id)
    return redirect("/")

@app.route('/acerca')
def acerca_de():
    """
    Ruta para la página "Acerca de"
    Muestra información sobre la aplicación
    """
    return render_template("acerca.html")

@app.route('/filtrar/<filtro>')
def tareas_filtradas(filtro):
    """
    FILTRAR TAREAS POR NOMBRE
    -------------------------
    Ruta para filtrar tareas
    El parámetro <filtro> en la URL se pasa como argumento a la función
    """
    # Obtenemos todas las tareas desde la base de datos
    filas = Tarea.get_all()
    # Filtramos por nombre conteniendo el filtro (insensible a mayúsculas)
    tareas_filtradas = [fila["nombre"] for fila in filas if filtro.lower() in fila["nombre"].lower()]
    return render_template("tareas.html", tarea=tareas_filtradas)