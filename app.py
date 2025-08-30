from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hola mundo desde la ruta"

@app.route("/acerca-de")
def tasks():
    return "<h1>Rutina.py</h1><p>Gestor de tareas para aprender programando con Python y Flask.</p>"

@app.route("/contacto")
def contact():
    return "Aquí se mostrará el formulario de contacto"

@app.route("/saludo")
def saludo():
    return "<h1>Hola mundo desde la ruta saludo</h1>"

@app.route("/saludo/<nombre>")
def saludo_nombre(nombre):
    return f"<h1>Hola {nombre}</h1>"