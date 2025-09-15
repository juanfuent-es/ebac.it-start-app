# Nombre de columna poco claro
"Fecha de Registro"

# Mejor
"fecha_registro"

# Formato inconsistente de fechas
"01/09/25", "2025-09-01"

# Mejor: formato único ISO # AAAA-MM-DD
"2025-09-01 00:00:00-06:00"
"09-13-2025" # No es ISO MM-DD-AAAA
"13-09-2025" # No es ISO DD-MM-AAAA

# Valores faltantes
"" # vacío
None # None

# Mejor
"NA"

# Booleanos ()
True
False
None # None