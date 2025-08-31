from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nueva-tarea", methods=["GET", "POST"])
def nueva_tarea():
    if request.method == "POST":
        nombre = request.form["title"]
        # return redirect("/tareas")
        return f"La tarea nueva es: {nombre}"
    else:
        return render_template("formulario.html")

@app.route("/tareas")
def mostrar_tareas():
    tareas = [
        {
            "nombre": "Hacer ejercicio",
            "estado": "pendiente",
            "prioridad": "alta",
            "fecha": "2025-08-24",
            "completada": False
        },
    ]
    return render_template("tareas.html", tareas=tareas)

@app.route('/acerca-de')
def acerca_de():
    return render_template("acerca-de.html")

@app.route('/filtrar-tareas/<filtro>')
def tareas_filtradas(filtro):
    return render_template("tareas.html", tareas=tareas_filtradas)