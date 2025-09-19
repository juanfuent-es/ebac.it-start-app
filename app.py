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
    """API que devuelve todas las tareas en formato JSON limpio"""
    registros = Tarea.get_all()
    categorias = { cat['id']: cat['nombre'] for cat in Categoria.get_all() }
    registros = [dict(fila) for fila in registros] # Convertir a diccionario
    for fila in registros:
        fila['categoria'] = categorias[fila['id_categoria']]
    return jsonify(registros)

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
    fecha_limite = data.get("fecha_limite")
    prioridad = data.get("prioridad")
    tiempo_estimado = data.get("tiempo_estimado")

    if nombre == "":
        return jsonify({"error": "El nombre de la tarea es obligatorio"}), 400
    if categoria == "":
        return jsonify({"error": "Debes proporcionar una 'categoria' válida"}), 400

    try:
        categoria_id = Categoria.get_or_create(categoria)
        Tarea.update(id, nombre)
        Tarea.move_to_categoria(id, categoria_id)
        
        # Actualizar nuevos campos si se proporcionan
        if fecha_limite is not None:
            Tarea.set_fecha_limite(id, fecha_limite)
        if prioridad is not None:
            Tarea.set_prioridad(id, prioridad)
        if tiempo_estimado is not None:
            Tarea.set_tiempo_estimado(id, tiempo_estimado)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    actualizado = Tarea.get_by_id(id)
    return jsonify(dict(actualizado))

@app.route('/api/tarea/<int:id>/toggle-estado', methods=["POST", "PATCH"])
def api_tareas_toggle_estado(id):
    """Alterna el estado de la tarea (pendiente <-> completada) y devuelve el registro actualizado como JSON."""
    registro = Tarea.get_by_id(id)
    if not registro:
        return jsonify({"error": "404: Tarea no encontrada"}), 404
    nuevo_estado = "pendiente" if registro["estado"] == "completada" else "completada"
    Tarea.set_estado(id, nuevo_estado)
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
    
    # Nuevos campos opcionales
    fecha_limite = data.get("fecha_limite")
    prioridad = data.get("prioridad")
    tiempo_estimado = data.get("tiempo_estimado")
    estado = data.get("estado", "pendiente")
    
    try:
        categoria_id = Categoria.get_or_create(categoria)
        new_id = Tarea.create(
            nombre=nombre, 
            id_categoria=categoria_id,
            estado=estado,
            fecha_limite=fecha_limite,
            prioridad=prioridad,
            tiempo_estimado=tiempo_estimado
        )
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
        fecha_limite = request.form.get("fecha_limite", "").strip() or None
        prioridad = request.form.get("prioridad", "").strip() or None
        tiempo_estimado = request.form.get("tiempo_estimado", "").strip() or None
        
        # Convertir tiempo_estimado a entero si se proporciona
        if tiempo_estimado:
            try:
                tiempo_estimado = int(tiempo_estimado)
            except ValueError:
                flash("El tiempo estimado debe ser un número válido", "danger")
                return redirect("/crear")
        
        try:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.create(
                nombre=nombre, 
                id_categoria=categoria_id,
                fecha_limite=fecha_limite,
                prioridad=prioridad,
                tiempo_estimado=tiempo_estimado
            )
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
    categoria = Categoria.get_by_id(tarea["id_categoria"])
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
    
    # Si es una petición AJAX (JSON), manejar con API
    if request.is_json:
        return api_tareas_show(id)
    
    if request.method == "POST":
        nombre = request.form.get("title", "").strip()
        categoria = request.form.get("categoria", "").strip()
        fecha_limite = request.form.get("fecha_limite", "").strip() or None
        prioridad = request.form.get("prioridad", "").strip() or None
        tiempo_estimado = request.form.get("tiempo_estimado", "").strip() or None
        
        # Convertir tiempo_estimado a entero si se proporciona
        if tiempo_estimado:
            try:
                tiempo_estimado = int(tiempo_estimado)
            except ValueError:
                flash("El tiempo estimado debe ser un número válido", "danger")
                return redirect(f"/editar/{id}")
        
        try:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.update(id, nombre)
            Tarea.move_to_categoria(id, categoria_id)
            
            # Actualizar nuevos campos
            if fecha_limite is not None:
                Tarea.set_fecha_limite(id, fecha_limite)
            if prioridad is not None:
                Tarea.set_prioridad(id, prioridad)
            if tiempo_estimado is not None:
                Tarea.set_tiempo_estimado(id, tiempo_estimado)
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

# =============================================================================
# CONFIGURACIÓN PARA DESPLIEGUE CON GUNICORN
# =============================================================================
# Esta variable es requerida por Gunicorn cuando despliega la aplicación
application = app

if __name__ == "__main__":
    # Solo ejecutar en modo desarrollo
    app.run(debug=True)