# Estructuras de datos

# Listas

tareas = ["Hacer ejercicio", "Leer", "Escribir"]
edades = [20, 21, 22]

print("DEMO: LISTAS")
print("########################################################")

tareas.append("Hacer de comer")
print(tareas)

tareas.remove("Leer")
print(tareas)

tareas.pop(0)
print(tareas)

tareas.clear()
print(tareas)

# Diccionarios
tarea = {
    "nombre": "Hacer ejercicio",
    "estado": "pendiente",
    "prioridad": "alta",
    "fecha": "2025-08-24"
}

print("########################################################")
print("DEMO: DICCIONARIOS")
print(f"La tarea es: {tarea['nombre']}")
print(f"La prioridad es: {tarea['prioridad']}")

print(tarea.keys())
print(tarea.values())
print(tarea.items())
print(tarea.get("fecha", "No hay fecha"))
print(tarea.items())

tarea.update({"estado": "completada"})
print(f"El estado de la tarea es: {tarea['estado']}")

tarea.pop("fecha")
print(tarea)

tarea.clear()
print(tarea)

print("########################################################")
print("DEMO: TUPLAS")

materias = ("Matemáticas", "Física", "Química", "Historia", "Física")
print(materias[3])

print(materias.count("Física"))

print("########################################################")
print("DEMO: CONJUNTOS")

numeros = {1, 2, 3, 4, 5, 3}
print(numeros)
