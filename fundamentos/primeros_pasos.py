# Así se define un comentario de una sola línea.
# Si me quieres descomentar quítame el #.

# Indentación / Sangrado
def saludar(nombre):
    print(f"Hola, {nombre}!")

#saludar("Juan") # Así se llama a la función

# Variables más comunes
nombre = "Juan" # Así se define una variable tipo 'String'
edad = 36 # Definición de una variable tipo 'Entero'
altura = 1.75 # Definición de una variable tipo 'Flotante'
completado = True # False | True - Definición de una variable tipo 'Booleano'

# print(nombre, edad, altura, completado)

# Operaciones básicas matemáticas
a = 10
b = 5

suma = a + b
resta = a - b
multiplicacion = a * b
division = a / b
potencia = a ** b
modulo = a % b

# Concatenación de cadenas de texto

# Concatenación de cadenas de texto. Clásica, funcional pero poco eficiente.
print("La suma de " + str(a) + " + " + str(b) + " es " + str(suma))
# f-string *Recomendada* - Manera más sencilla de concatenar cadenas de texto.
print(f"La resta de {a} - {b} es {resta}")

# Nomenclatura de variables

# En python podemos empezar a definir variables con letras y guiones bajos, pero no con números.
# Usemos nombres descriptivos y claros. Usar snake_case.

color_r = 0 # Red
color_g = 255 # Green
color_b = 125 # Blue

hi_en = "Hola"
hi_es = "Hola"