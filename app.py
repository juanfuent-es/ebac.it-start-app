from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nueva-tarea", methods=["GET", "POST"])
def nueva_tarea():
    if request.method == "POST":
        nombre = request.form["title"]
        # return redirect("/tareas")
        tareas = request.cookies.get("tareas", "")
        # Ej: Cookie:tareas = "Barrer,Limpiar,Estudiar"
        lista = tareas.split(",") if tareas else []
        lista.append(nombre)
        # Ej: Cookie:tareas = ["Barrer","Limpiar","Estudiar","Hacer ejercicio"]
        response = make_response(redirect("/tareas"))
        # Ej: Cookie:tareas = "Barrer,Limpiar,Estudiar,Hacer ejercicio"
        response.set_cookie("tareas", ",".join(lista))
        return response
    else:
        return render_template("formulario.html")

@app.route("/tareas")
def mostrar_tareas():
    tareas = request.cookies.get("tareas", "")
    lista_tareas = tareas.split(",") if tareas else []
    return render_template("tareas.html", tareas=lista_tareas)

@app.route('/acerca-de')
def acerca_de():
    return render_template("acerca-de.html")

@app.route('/filtrar-tareas/<filtro>')
def tareas_filtradas(filtro):
    return render_template("tareas.html", tareas=tareas_filtradas)