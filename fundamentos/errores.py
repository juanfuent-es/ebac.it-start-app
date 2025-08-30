# Debugging Errors

# SyntaxError:

if 10 > 5:
    print("10 es mayor que 5")
else:
    print("10 no es mayor que 5")

# Error de lógica
def es_par(numero):
    return numero % 2 == 0

par = es_par(10)
print(f"El número 10 es par: {par}")

# Errores de ejecución
numeros = [1, 2, 3, 4, 5]
print(numeros[4])

# Depuración de errores

# Esta función divide dos números y maneja el error de división por cero
def dividir(a, b):
    print(f"Dividiendo {a} entre {b}")
    try:
        return a / b
    except ZeroDivisionError:
        print("No se puede dividir por cero")
        return 0

resultado = dividir(10, 0)
print(resultado)

# Depuración de errores