# Funciones / Entrada / Salida

# Definición de una función
def saludar(nombre): # 'nombre' es un parámetro
    print(f"Hola, {nombre} ¿cómo estás?")

# Llamada a una función
saludar("Juan") # 'Juan' es un argumento
saludar("Pedro") # 'Pedro' es un argumento
saludar("María") # 'Maria' es un argumento

def sumar(a, b): # 'a' y 'b' son parámetros
    return a + b # 'return' es una palabra reservada que devuelve el resultado de la función

resultado = sumar(10, 20) # '10' y '20' son argumentos
print(resultado)

print("########################################################")
print("DEMO: ENTRADA Y SALIDA DE DATOS")

tareas = []

def mostrar_tareas():
    print("Tareas:")
    for tarea in tareas:
        print(f"- {tarea}")

def agregar_tarea():
    tarea = input("Ingrese la tarea: ")
    if tarea.strip() != "":
        tareas.append(tarea)
        print(f"Tarea agregada: {tarea}")
        mostrar_tareas()
    else:
        print("No se puede agregar una tarea vacía")

agregar_tarea()