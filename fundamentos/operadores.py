# Operadores aritméticos
a = 10
b = 5

suma = a + b
resta = a - b
multiplicacion = a * b
division = a / b
potencia = a ** b
modulo = a % b

print("########################################################")
print("DEMO: OPERADORES ARITMÉTICOS")
print("########################################################")
print("Suma: ", suma)
print("Resta: ", resta)
print("Multiplicación: ", multiplicacion)
print("División: ", division)
print("Potencia: ", potencia)
print("Módulo: ", modulo)

# Operadores de comparación
print("########################################################")
print("DEMO: OPERADORES DE COMPARACIÓN")
print("########################################################")
print("'a' es igual a 'b': ", a == b) # False
print("'a' es diferente a 'b': ", a != b) # True
print("'a' es mayor que 'b': ", a > b) # True
print("'a' es mayor o igual que 'b': ", a >= b) # True
print("'a' es menor que 'b': ", a < b) # False
print("'a' es menor o igual que 'b': ", a <= b) # False

# Operadores lógicos
x = 8
y = 5

print("########################################################")
print("DEMO: OPERADORES LÓGICOS")
print("########################################################")
print("x es mayor que y 'and' x es menor que y: ", x > y and y > 2)
print("x es mayor que y 'or' x es menor que y: ", x > y or y > 2)
print("x es mayor que y 'not' x es menor que y: ", not x == 8)

print("########################################################")
print("EJEMPLOS DE GESTOR DE TAREAS")
print("########################################################")

tarea_completada = False
urgente = True

print("La tarea está completada: ", tarea_completada)
print("La tarea es urgente: ", urgente)
print("¿La tarea está completada y es urgente? ", tarea_completada and urgente)