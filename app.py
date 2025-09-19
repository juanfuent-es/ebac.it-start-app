import os
from flask import Flask, render_template, request, redirect, flash, Response
from database import init_db
from models.categoria import Categoria
from models.tarea import Tarea

app = Flask(__name__)

def requires_auth(f):
    def decorated(*args, **kwargs):
        if os.environ.get('ENVIRONMENT') == 'production':
            auth = request.authorization
            username = os.environ.get('USERNAME')
            password = os.environ.get('PASSWORD')
            
            if not auth or auth.username != username or auth.password != password:
                return Response('Acceso denegado', 401, {'WWW-Authenticate': 'Basic realm="Login"'})
        return f(*args, **kwargs)
    return decorated

init_db()

@app.route("/")
@requires_auth
def index():
    registros = Tarea.get_all()
    return render_template("index.html", tareas=registros)

@app.route("/crear", methods=["GET", "POST"])
@requires_auth
def nueva_tarea():
    if request.method == "POST":
        nombre = request.form.get("title", "").strip()
        categoria = request.form.get("categoria", "").strip()
        
        if nombre and categoria:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.create(nombre=nombre, id_categoria=categoria_id)
            flash("Tarea creada correctamente", "success")
            return redirect("/")
        else:
            flash("Nombre y categoría son obligatorios", "danger")
    
    categorias = Categoria.get_all()
    return render_template("formulario.html", categorias=categorias)

@app.route('/tarea/<int:id>')
@requires_auth
def detalle(id):
    tarea = Tarea.get_by_id(id)
    if not tarea:
        return "Tarea no encontrada", 404
    categoria = Categoria.get_by_id(tarea["id_categoria"])
    return render_template("tarea.html", tarea=tarea, categoria=categoria)

@app.route('/tarea/<int:id>/toggle-estado', methods=["POST"])
@requires_auth
def toggle_estado(id):
    tarea = Tarea.get_by_id(id)
    if tarea:
        nuevo_estado = "pendiente" if tarea["estado"] == "completada" else "completada"
        Tarea.set_estado(id, nuevo_estado)
    return redirect(f"/tarea/{id}")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@requires_auth
def editar(id):
    tarea = Tarea.get_by_id(id)
    if not tarea:
        return "Tarea no encontrada", 404
    
    if request.method == "POST":
        nombre = request.form.get("title", "").strip()
        categoria = request.form.get("categoria", "").strip()
        
        if nombre and categoria:
            categoria_id = Categoria.get_or_create(categoria)
            Tarea.update(id, nombre)
            Tarea.move_to_categoria(id, categoria_id)
            flash("Tarea actualizada", "success")
            return redirect(f"/tarea/{id}")
        else:
            flash("Nombre y categoría son obligatorios", "danger")
    
    categorias = Categoria.get_all()
    return render_template("editar.html", tarea=tarea, categorias=categorias)

@app.route("/eliminar/<int:id>")
@requires_auth
def eliminar(id):
    Tarea.delete(id)
    return redirect("/")

@app.route('/acerca')
@requires_auth
def acerca_de():
    return render_template("acerca.html")

if __name__ == "__main__":
    app.run(debug=True)