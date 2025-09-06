# =============================================================================
# APLICACIÓN WEB FLASK - GESTOR DE TAREAS
# =============================================================================
# Este archivo contiene la lógica principal de nuestra aplicación web
# Flask es un framework web ligero para Python que nos permite crear
# aplicaciones web de forma sencilla

# Importamos las clases y funciones que necesitamos de Flask
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from models.categoria import Categoria
from models.tarea import Tarea

# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial de Python que contiene el nombre del módulo
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev")

# =============================================================================
# DEFINICIÓN DE RUTAS (ROUTES)
# =============================================================================
# Las rutas son las URLs que los usuarios pueden visitar en nuestro sitio web
# Cada ruta está asociada a una función que se ejecuta cuando se visita esa URL

@app.route("/")
def index():
    """Página de inicio: lista tareas desde BD (JOIN con categoría)."""
    tareas = Tarea.with_categoria()
    categorias = Categoria.get_all()
    return render_template("index.html", tareas=tareas, categorias=categorias)

@app.route("/nueva-tarea", methods=["GET", "POST"])
def nueva_tarea():
    """Crear tarea en BD."""
    if request.method == "POST":
        nombre = request.form.get("title", "").strip()
        categoria_id = int(request.form.get("categoria_id"))
        if not nombre:
            flash("El nombre es obligatorio", "warning")
            return redirect(url_for("nueva_tarea"))
        Tarea.create(nombre, categoria_id)
        return redirect(url_for("mostrar_tareas"))
    categorias = Categoria.get_all()
    return render_template("formulario.html", categorias=categorias)

@app.route("/tareas")
def mostrar_tareas():
    """Lista de tareas desde BD (JOIN con categorías)."""
    tareas = Tarea.with_categoria()
    return render_template("tareas.html", tareas=tareas)

@app.route('/acerca-de')
def acerca_de():
    """
    Ruta para la página "Acerca de"
    Muestra información sobre la aplicación
    """
    return render_template("acerca-de.html")

@app.route('/filtrar-tareas/<estado>')
def tareas_filtradas(estado):
    """Filtra tareas por estado."""
    estado = estado.strip().lower()
    todas = Tarea.with_categoria()
    filtradas = [t for t in todas if t[2].lower() == estado]  # (id,nombre,estado,categoria_id,categoria,created,updated)
    return render_template("tareas.html", tareas=filtradas)

@app.route("/editar-tarea/<int:tarea_id>", methods=["GET", "POST"])
def editar_tarea(tarea_id):
    """Editar tarea en BD."""
    if request.method == "POST":
        nuevo_nombre = request.form.get("title", "").strip()
        if not nuevo_nombre:
            return redirect(url_for("editar_tarea", tarea_id=tarea_id))
        Tarea.update(tarea_id, nuevo_nombre)
        return redirect(url_for("mostrar_tareas"))
    fila = Tarea.get_by_id(tarea_id)
    if not fila:
        return redirect(url_for("mostrar_tareas"))
    # fila: (id, nombre, estado, categoria_id, created_at, updated_at)
    return render_template("editar_tarea.html", tarea=fila[1], indice=tarea_id)

@app.route("/eliminar-tarea/<int:tarea_id>")
def eliminar_tarea(tarea_id):
    """Eliminar tarea en BD."""
    Tarea.delete(tarea_id)
    return redirect(url_for("mostrar_tareas"))


# =============================================================================
# CRUD de Categorías
# =============================================================================

@app.route("/categorias")
def listar_categorias():
    categorias = Categoria.get_all()
    return render_template("categorias.html", categorias=categorias)


@app.route("/nueva-categoria", methods=["GET", "POST"])
def nueva_categoria():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio", "warning")
            return redirect(url_for("nueva_categoria"))
        try:
            Categoria.create(nombre)
        except sqlite3.IntegrityError:
            flash("Ya existe una categoría con ese nombre", "warning")
            return redirect(url_for("nueva_categoria"))
        return redirect(url_for("listar_categorias"))
    return render_template("form_categoria.html")


@app.route("/editar-categoria/<int:categoria_id>", methods=["GET", "POST"])
def editar_categoria(categoria_id: int):
    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre", "").strip()
        if not nuevo_nombre:
            return redirect(url_for("editar_categoria", categoria_id=categoria_id))
        try:
            Categoria.update(categoria_id, nuevo_nombre)
        except sqlite3.IntegrityError:
            flash("Ya existe una categoría con ese nombre", "warning")
            return redirect(url_for("editar_categoria", categoria_id=categoria_id))
        return redirect(url_for("listar_categorias"))
    categoria = Categoria.get_by_id(categoria_id)
    if not categoria:
        return redirect(url_for("listar_categorias"))
    # categoria: (id, nombre, created_at, updated_at)
    return render_template("form_categoria.html", categoria=categoria)


@app.route("/eliminar-categoria/<int:categoria_id>")
def eliminar_categoria(categoria_id: int):
    try:
        Categoria.delete(categoria_id)
    except sqlite3.IntegrityError:
        flash("No se puede eliminar: la categoría tiene tareas asociadas", "warning")
    return redirect(url_for("listar_categorias"))

# =============================================================================
# CONFIGURACIÓN PARA EJECUTAR LA APLICACIÓN
# =============================================================================
# Esta línea solo se ejecuta si ejecutamos este archivo directamente
# (no si lo importamos desde otro archivo)
if __name__ == "__main__":
    # debug=True activa el modo de desarrollo
    # - Muestra errores detallados en el navegador
    # - Reinicia automáticamente el servidor cuando cambias el código
    # - Solo debe usarse en desarrollo, no en producción
    app.run(debug=True)