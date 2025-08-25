# Estructuras de control

tarea = "Hacer ejercicio"

if tarea == "Leer":
    print("Disfruta tu lectura")
else:
    print("Suerte en la ejecución de la tarea")

tareas = ["Hacer ejercicio", "Leer", "Escribir"]

print("########################################################")
print("DEMO: BUCLE FOR")    
print("########################################################")
for tarea in tareas:
    print(f"La tarea es: {tarea}")

print("########################################################")
print("DEMO: BUCLE WHILE")
print("########################################################")

contador = 10

while contador <= 10:
    print(f"El contador es: {contador}")
    contador += 1