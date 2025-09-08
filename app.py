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
from flask import Flask, render_template, request, redirect, flash
import sqlite3
from database import init_db
from models.categoria import Categoria
from models.tarea import Tarea
# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial de Python que contiene el nombre del módulo
app = Flask(__name__)
app.secret_key = "dev-secret"  # Necesario para usar mensajes flash
init_db()

# =============================================================================
# ESQUEMATIZA TUS RUTAS CRUD - Crear, Leer, Actualizar, Eliminar
# =============================================================================
# Las rutas son las URLs que los usuarios pueden visitar en nuestro sitio web.
# Esquema general del CRUD:
#   - GET  /                        -> Listar todas las tareas registradas
#   - GET  /crear                   -> Formulario: crear nueva tarea
#   - POST /crear                   -> Crear una nueva tarea desde formulario web
#   - GET  /tarea/<id>              -> Consulta el detalle de una tarea específica
#   - GET  /editar/<id>             -> Edita una tarea existente (vista)
#   - POST /editar/<id>             -> Actualiza una tarea existente
#   - GET  /eliminar/<id>           -> Elimina una tarea desde la interfaz
#   - GET  /filtrar/<filtro>        -> Listado filtrado por categoría o estado
#   - GET  /acerca                  -> Página "Acerca de"

@app.route("/")
def index():
    registros = Tarea.get_all()
    return render_template("index.html", tareas=registros)

@app.route("/crear", methods=["GET", "POST"])
def nueva_tarea():
    if request.method == "POST": # Verificamos si la petición es POST (envío de formulario)
        nombre = request.form.get("title", "").strip()
        categoria = request.form.get("categoria", "").strip()
        try:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.create(nombre=nombre, categoria_id=categoria_id)
        except ValueError as err:
            flash(str(err), "danger")
            return redirect(f"/crear")
        flash("Tarea creada correctamente", "success")
        return redirect("/")
    else:
        categorias = Categoria.get_all()
        return render_template("formulario.html", categorias=categorias)

@app.route('/tarea/<int:id>')
def detalle(id): # CONSULTA EL DETALLE DE UNA TAREA ESPECÍFICA
    tarea = Tarea.get_by_id(id)
    categoria = Categoria.get_by_id(tarea["categoria_id"])
    return render_template("tarea.html", tarea=tarea, categoria=categoria)

@app.route('/tarea/<int:id>/toggle-estado', methods=["POST"])
def toggle_estado(id): # Alterna el estado de la tarea entre 'pendiente' y 'completada'
    tarea = Tarea.get_by_id(id)
    if not tarea:
        return redirect("/")
    nuevo_estado = "pendiente" if tarea["estado"] == "completada" else "completada"
    Tarea.set_estado(id, nuevo_estado)
    return redirect(f"/tarea/{id}")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id): # EDITA Y ACTUALIZA UNA TAREA EXISTENTE
    tarea = Tarea.get_by_id(id)
    if request.method == "POST":
        nombre = request.form.get("title", "")
        categoria = Categoria.get_or_create(request.form.get("categoria"))
        try:
            nombre_ok, categoria_ok = Tarea.validate(nombre, categoria["id"])
        except ValueError as err:
            flash(str(err), "danger")
            return redirect(f"/editar/{id}?nombre={nombre}&categoria={(categoria and categoria['nombre']) or ''}")
        # Actualizamos nombre
        Tarea.update(id, str(nombre_ok).strip())
        # Movemos de categoría si cambió
        if categoria_ok != tarea["categoria_id"]:
            try:
                Tarea.move_to_categoria(id, categoria_ok)
            except sqlite3.IntegrityError:
                flash("No se pudo cambiar la categoría por una restricción de integridad.", "danger")
                return redirect(f"/editar/{id}")
        flash("Tarea actualizada", "success")
        return redirect(f"/tarea/{id}")
    else:
        # Pasamos datos necesarios: nombre, índice, categorías y categoría actual
        categorias = Categoria.get_all()
        # Posible prefill desde query params
        nombre_q = request.args.get("nombre")
        categoria_q = request.args.get("categoria")
        if nombre_q is not None:
            tarea = dict(tarea)
            tarea["nombre"] = nombre_q
        if categoria_q is not None:
            tarea = dict(tarea)
            tarea["categoria_id"] = categoria_q
        return render_template(
            "editar.html",
            tarea=tarea,
            categorias=categorias
        )

@app.route("/eliminar/<int:id>")
def eliminar(id): # ELIMINA UNA TAREA DESDE LA INTERFAZ
    tarea = Tarea.get_by_id(id)
    if tarea:
        Tarea.delete(id)
    return redirect("/")

@app.route('/acerca')
def acerca_de():
    return render_template("acerca.html")

@app.route('/filtrar/<filtro>')
def tareas_filtradas(filtro):
    # Obtenemos todas las tareas desde la base de datos
    filas = Tarea.get_all()
    # Filtramos por nombre conteniendo el filtro (insensible a mayúsculas)
    tareas_filtradas = [fila["nombre"] for fila in filas if filtro.lower() in fila["nombre"].lower()]
    return render_template("tareas.html", tarea=tareas_filtradas)