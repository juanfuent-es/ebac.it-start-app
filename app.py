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
from flask import Flask, render_template, request, redirect, flash, abort, jsonify
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

# =============================================================================
# API JSON - 'Endpoints' para Tarea (CRUD)
# =============================================================================
@app.route('/api/tareas', methods=["GET"])
def api_tareas_index():
    registros = Tarea.get_all()
    return jsonify([{"id": fila["id"], "nombre": fila["nombre"]} for fila in registros])

@app.route('/api/tarea/<int:id>', methods=["GET", "PUT", "PATCH", "DELETE"])
def api_tareas_show(id):
    registro = Tarea.get_by_id(id)
    if not registro:
        return jsonify({"error": "404: Tarea no encontrada"}), 404
    if request.method == "GET":
        return jsonify(dict(registro))
    if request.method == "DELETE":
        Tarea.delete(id)
        return ("", 204)
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400
    data = request.get_json(silent=True) or {}

    nombre = str(data.get("nombre", "")).strip()
    categoria = str(data.get("categoria", "")).strip()

    if nombre == "":
        return jsonify({"error": "El nombre de la tarea es obligatorio"}), 400
    if categoria == "":
        return jsonify({"error": "Debes proporcionar una 'categoria' válida"}), 400

    try:
        categoria_id = Categoria.get_or_create(categoria)
        Tarea.update(id, nombre)
        Tarea.move_to_categoria(id, categoria_id)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    actualizado = Tarea.get_by_id(id)
    return jsonify(dict(actualizado))

@app.route('/api/tareas', methods=["POST"])
def api_tareas_create():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400
    data = request.get_json(silent=True) or {}

    nombre = str(data.get("nombre", "")).strip()
    if nombre == "":
        return jsonify({"error": "El nombre de la tarea es obligatorio"}), 400
    categoria = str(data.get("categoria", "")).strip()
    if categoria == "":
        return jsonify({"error": "Debes proporcionar una 'categoria' válida"}), 400
    try:
        categoria_id = Categoria.get_or_create(categoria)
        new_id = Tarea.create(nombre=nombre, categoria_id=categoria_id)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    nueva = Tarea.get_by_id(new_id)
    return jsonify(dict(nueva)), 201

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
    if not tarea:
        return render_template("404.html"), 404
    categoria = Categoria.get_by_id(tarea["categoria_id"])
    return render_template("tarea.html", tarea=tarea, categoria=categoria)

@app.route('/tarea/<int:id>/toggle-estado', methods=["POST"])
def toggle_estado(id): # Alterna el estado de la tarea entre 'pendiente' y 'completada'
    tarea = Tarea.get_by_id(id)
    if not tarea:
        return render_template("404.html"), 404
    nuevo_estado = "pendiente" if tarea["estado"] == "completada" else "completada"
    Tarea.set_estado(id, nuevo_estado)
    return redirect(f"/tarea/{id}")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id): # EDITA Y ACTUALIZA UNA TAREA EXISTENTE
    tarea = Tarea.get_by_id(id)
    if not tarea:
        abort(404)
        return render_template("404.html"), 404
    if request.method == "POST":
        nombre = request.form.get("title", "").strip()
        categoria = request.form.get("categoria", "").strip()
        try:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.update(id, nombre)
            Tarea.move_to_categoria(id, categoria_id)
        except ValueError as err:
            flash(str(err), "danger")
            return redirect(f"/editar/{id}")
        flash("Tarea actualizada", "success")
        return redirect(f"/tarea/{id}")
    else:
        categorias = Categoria.get_all()
        return render_template("editar.html", tarea=tarea, categorias=categorias)

@app.route("/eliminar/<int:id>")
def eliminar(id): # ELIMINA UNA TAREA DESDE LA INTERFAZ
    tarea = Tarea.get_by_id(id)
    if tarea:
        Tarea.delete(id)
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route('/acerca')
def acerca_de():
    return render_template("acerca.html")

@app.route('/filtrar/<filtro>')
def tareas_filtradas(filtro):
    # Obtenemos todas las tareas desde la base de datos
    filas = Tarea.get_all()
    # Filtramos por nombre conteniendo el filtro (insensible a mayúsculas)
    return render_template("tareas.html", tarea=filas)
