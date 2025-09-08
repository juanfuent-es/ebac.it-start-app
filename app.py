# =============================================================================
# APLICACIÓN WEB FLASK - GESTOR DE TAREAS
# =============================================================================
# Este archivo contiene la lógica principal de nuestra aplicación web
# Flask es un framework web ligero para Python que nos permite crear
# aplicaciones web de forma sencilla

# Importamos las clases y funciones que necesitamos de Flask
from flask import Flask, render_template, request, redirect, make_response

# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial de Python que contiene el nombre del módulo
app = Flask(__name__)

# =============================================================================
# DEFINICIÓN DE RUTAS (ROUTES)
# =============================================================================
# Las rutas son las URLs que los usuarios pueden visitar en nuestro sitio web
# Cada ruta está asociada a una función que se ejecuta cuando se visita esa URL

@app.route("/")
def index():
    """
    Ruta principal de la aplicación (página de inicio)
    Cuando alguien visita http://localhost:5000/ se ejecuta esta función
    """
    # render_template() busca el archivo HTML en la carpeta 'templates'
    # y lo devuelve como respuesta al navegador
    return render_template("index.html")

@app.route("/nueva-tarea", methods=["GET", "POST"])
def nueva_tarea():
    """
    Ruta para crear nuevas tareas
    - GET: Muestra el formulario para crear una tarea
    - POST: Procesa los datos del formulario y guarda la tarea
    """
    # Verificamos si la petición es POST (envío de formulario)
    if request.method == "POST":
        # Obtenemos el título de la tarea desde el formulario
        # request.form es un diccionario que contiene los datos enviados
        nombre = request.form["title"]
        
        # OBTENEMOS LAS TAREAS EXISTENTES DESDE LAS COOKIES
        # Las cookies son pequeños archivos que se guardan en el navegador del usuario
        # get() devuelve el valor de la cookie o una cadena vacía si no existe
        tareas = request.cookies.get("tareas", "")
        estados = request.cookies.get("estados", "")
        categorias = request.cookies.get("categorias", "")
        
        # CONVERTIMOS LA CADENA DE TAREAS EN UNA LISTA
        # Ejemplo: "Barrer,Limpiar,Estudiar" -> ["Barrer", "Limpiar", "Estudiar"]
        # Si no hay tareas, creamos una lista vacía
        lista = tareas.split(",") if tareas else []
        lista_estados = estados.split(",") if estados else []
        lista_categorias = categorias.split(",") if categorias else []
        
        # AGREGAMOS LA NUEVA TAREA A LA LISTA
        lista.append(nombre)
        # Inicializamos estado y categoría por defecto
        lista_estados.append("pendiente")
        lista_categorias.append("-")
        
        # CREAMOS UNA RESPUESTA DE REDIRECCIÓN
        # make_response() nos permite crear una respuesta personalizada
        # redirect() redirige al usuario a otra página
        response = make_response(redirect("/tareas"))
        
        # GUARDAMOS LA LISTA ACTUALIZADA EN LAS COOKIES
        # join() convierte la lista en una cadena separada por comas
        # set_cookie() guarda la información en el navegador del usuario
        response.set_cookie("tareas", ",".join(lista))
        response.set_cookie("estados", ",".join(lista_estados))
        response.set_cookie("categorias", ",".join(lista_categorias))
        
        return response
    else:
        # Si la petición es GET, mostramos el formulario
        return render_template("formulario.html")

@app.route("/tareas")
def mostrar_tareas():
    """
    Ruta para mostrar todas las tareas guardadas
    Lee las tareas desde las cookies y las muestra en una página
    """
    # Obtenemos las tareas desde las cookies
    tareas = request.cookies.get("tareas", "")
    
    # Convertimos la cadena en una lista
    lista_tareas = tareas.split(",") if tareas else []
    
    # Pasamos la lista de tareas al template para mostrarlas
    # El segundo parámetro (tareas=lista_tareas) hace que la variable
    # 'tareas' esté disponible en el template HTML
    return render_template("tareas.html", tareas=lista_tareas)

@app.route("/tarea/<int:indice>")
def detalle_tarea(indice: int):
    """
    Muestra el detalle de una tarea: nombre, estado y categoría.
    """
    tareas = request.cookies.get("tareas", "")
    estados = request.cookies.get("estados", "")
    categorias = request.cookies.get("categorias", "")

    lista_tareas = tareas.split(",") if tareas else []
    lista_estados = estados.split(",") if estados else []
    lista_categorias = categorias.split(",") if categorias else []

    if indice >= len(lista_tareas):
        return redirect("/tareas")

    tarea_actual = lista_tareas[indice]
    estado_actual = lista_estados[indice] if indice < len(lista_estados) else "pendiente"
    categoria_nombre = lista_categorias[indice] if indice < len(lista_categorias) else "-"

    return render_template(
        "tarea.html",
        tarea=tarea_actual,
        estado=estado_actual,
        categoria_nombre=categoria_nombre,
        indice=indice,
    )

@app.route("/tarea/<int:indice>/actualizar-estado", methods=["POST"]) 
def actualizar_estado_tarea(indice: int):
    """
    Actualiza el estado de una tarea (p.ej., de pendiente a listo) y redirige al detalle.
    """
    nuevo_estado = request.form.get("nuevo_estado", "listo")

    estados = request.cookies.get("estados", "")
    lista_estados = estados.split(",") if estados else []

    tareas = request.cookies.get("tareas", "")
    lista_tareas = tareas.split(",") if tareas else []

    if indice >= len(lista_tareas):
        return redirect("/tareas")

    # Aseguramos largo de estados
    while len(lista_estados) < len(lista_tareas):
        lista_estados.append("pendiente")

    lista_estados[indice] = nuevo_estado

    response = make_response(redirect(f"/tarea/{indice}"))
    response.set_cookie("estados", ",".join(lista_estados))
    return response

@app.route('/acerca-de')
def acerca_de():
    """
    Ruta para la página "Acerca de"
    Muestra información sobre la aplicación
    """
    return render_template("acerca-de.html")

@app.route('/filtrar-tareas/<filtro>')
def tareas_filtradas(filtro):
    """
    Ruta para filtrar tareas (FUNCIONALIDAD INCOMPLETA)
    El parámetro <filtro> en la URL se pasa como argumento a la función
    """
    # NOTA: Esta función no está implementada completamente
    # tareas_filtradas no está definida, lo que causaría un error
    return render_template("tareas.html", tareas=tareas_filtradas)

@app.route("/editar-tarea/<int:indice>", methods=["GET", "POST"])
def editar_tarea(indice):
    """
    Ruta para editar una tarea específica
    - <int:indice>: Convierte el parámetro de la URL en un número entero
    - GET: Muestra el formulario con la tarea actual
    - POST: Guarda los cambios de la tarea
    """
    # Obtenemos la lista actual de tareas
    tareas = request.cookies.get("tareas", "")
    lista_tareas = tareas.split(",") if tareas else []
    
    # VERIFICACIÓN DE SEGURIDAD
    # Nos aseguramos de que el índice sea válido
    if indice >= len(lista_tareas):
        return redirect("/tareas")
    
    if request.method == "POST":
        # Procesamos el formulario de edición
        nuevo_nombre = request.form["title"]
        
        # ACTUALIZAMOS LA TAREA EN LA LISTA
        lista_tareas[indice] = nuevo_nombre
        
        # Guardamos la lista actualizada en las cookies
        response = make_response(redirect("/tareas"))
        response.set_cookie("tareas", ",".join(lista_tareas))
        return response
    else:
        # Mostramos el formulario de edición
        tarea_actual = lista_tareas[indice]
        
        # Pasamos tanto la tarea como el índice al template
        # para que el formulario sepa qué tarea está editando
        return render_template("editar_tarea.html", tarea=tarea_actual, indice=indice)

@app.route("/eliminar-tarea/<int:indice>")
def eliminar_tarea(indice):
    """
    Ruta para eliminar una tarea específica
    Elimina la tarea del índice especificado y redirige a la lista
    """
    # Obtenemos la lista actual de tareas
    tareas = request.cookies.get("tareas", "")
    lista_tareas = tareas.split(",") if tareas else []
    
    # VERIFICACIÓN DE SEGURIDAD
    # Solo eliminamos si el índice es válido
    if indice < len(lista_tareas):
        # pop() elimina y devuelve el elemento en el índice especificado
        lista_tareas.pop(indice)
        
        # Guardamos la lista actualizada en las cookies
        response = make_response(redirect("/tareas"))
        response.set_cookie("tareas", ",".join(lista_tareas))
        return response
    
    # Si el índice no es válido, redirigimos a la lista de tareas
    return redirect("/tareas")

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