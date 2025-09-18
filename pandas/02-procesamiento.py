# Importamos las librerías necesarias para el procesamiento de datos
import requests  # Para hacer peticiones HTTP a APIs
import pandas as pd  # Para manipular y analizar datos estructurados

# PASO 1: CARGAR DATOS DESDE LA API
# Hacemos una petición GET a la API de nuestra aplicación Flask
resp = requests.get("http://localhost:5000/api/tareas")

# Usamos try-except para manejar posibles errores de conexión
try:
    # Convertimos la respuesta JSON en un diccionario de Python
    datos = resp.json()
    
    # Creamos un DataFrame de pandas con los datos obtenidos
    # Un DataFrame es como una tabla de Excel pero programáticamente
    df = pd.DataFrame(datos)
    
    # Mostramos información básica sobre los datos cargados
    print("Datos cargados correctamente")
    print(f"Total de tareas: {len(df)}")  # Número total de filas
    print(f"Columnas disponibles: {list(df.columns)}")  # Nombres de las columnas
except Exception as e:
    # Si hay algún error, mostramos el mensaje y una sugerencia
    print(f"Error al cargar datos: {e}")
    print("Sugerencia: Asegúrate de que la aplicación Flask esté ejecutándose en localhost:5000")
    # Creamos un DataFrame vacío para evitar errores posteriores
    df = pd.DataFrame()

def limpiar_datos_basicos():
    """
    PASO 2: LIMPIEZA BÁSICA DE DATOS
    Esta función elimina datos problemáticos y normaliza el formato
    """
    print("Iniciando limpieza básica de datos...")
    
    # Guardamos el número inicial de filas para comparar después
    filas_iniciales = len(df)
    print(f"Estado inicial: {filas_iniciales} filas")
    
    # ELIMINACIÓN DE VALORES NULOS
    # dropna() elimina filas que tengan al menos un valor nulo
    # inplace=True modifica el DataFrame directamente
    df.dropna(inplace=True)
    filas_despues_nulos = len(df)
    print(f"Después de eliminar nulos: {filas_despues_nulos} filas")

    # CONVERSIÓN DE FECHAS A DATETIME
    # Convertimos las columnas de fecha de string a datetime
    # errors='coerce' convierte valores inválidos a NaT (Not a Time)
    columnas_fecha = ['fecha_creacion','fecha_limite','completado_en', 'fecha_actualizacion', 'fecha_limite']
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print(f"Formato de fecha corregido para: {columnas_fecha}")
    
    # NORMALIZACIÓN DE TEXTO
    # Convertimos el estado a minúsculas y eliminamos espacios extra
    # Esto evita problemas como "Pendiente" vs "pendiente" vs " pendiente "
    df['estado'] = df['estado'].str.lower().str.strip()
    print("Texto normalizado a minúsculas en columna 'estado'")
    print(f"Limpieza completada: {filas_iniciales - filas_despues_nulos} filas eliminadas")

def detectar_outliers():
    """
    PASO 3: DETECCIÓN DE OUTLIERS Y VALORES INCONSISTENTES
    Identificamos datos que pueden ser erróneos o problemáticos
    """
    print("Detectando outliers y valores inconsistentes...")    
    
    # DETECCIÓN DE TIEMPOS NEGATIVOS
    # Los tiempos estimados no pueden ser negativos
    tiempos_negativos = df[df['tiempo_estimado'] < 0]
    print(f"Tiempos estimados negativos: {len(tiempos_negativos)} casos")

    # DETECCIÓN DE FECHAS LÓGICAMENTE INCORRECTAS
    # Una tarea no puede completarse antes de ser creada
    fechas_incorrectas = df[df['completado_en'] < df['fecha_creacion']]
    print(f"Fechas incorrectas: {len(fechas_incorrectas)} casos")

    # ANÁLISIS DE VALORES ÚNICOS EN PRIORIDAD
    # Verificamos qué valores únicos existen en la columna prioridad
    # Esto ayuda a detectar inconsistencias como "alta", "Alta", "ALTA"
    prioridades_unicas = df['prioridad'].value_counts()
    print(f"Valores únicos en prioridad: {len(prioridades_unicas)}")
    print("Valores encontrados:", prioridades_unicas.index.tolist())

def crear_columnas_derivadas():
    """
    PASO 4: CREACIÓN DE COLUMNAS DERIVADAS
    Creamos nuevas columnas calculadas a partir de los datos existentes
    """
    print("Creando columnas derivadas...")
    
    # COLUMNA DE TAREAS ATRASADAS
    # Verificamos si la fecha de completado es posterior a la fecha límite
    df['atrasada'] = df['completado_en'] > df['fecha_limite']
    print(f"Columna 'atrasada' creada: {df['atrasada']}")
    
    # COLUMNA DE MES DE CREACIÓN
    # Extraemos el mes de la fecha de creación para análisis temporal
    df['mes'] = df['fecha_creacion'].dt.month
    print(f"Columna 'mes' creada: {df['mes']}")
    
    # COLUMNA DE SEMANA DE COMPLETADO
    # Extraemos la semana del año para análisis semanal
    df['semana'] = df['completado_en'].dt.isocalendar().week
    
    # COLUMNA DE DÍAS ENTRE CREACIÓN Y ENTREGA
    # Calculamos cuántos días transcurrieron desde la creación hasta la entrega
    df['dias_entre_creacion_y_entrega'] = (df['completado_en'] - df['fecha_creacion']).dt.days
    print(f"Columna 'dias_entre_creacion_y_entrega' creada: {df['dias_entre_creacion_y_entrega']}")
    
    # COLUMNA DE DURACIÓN REAL
    # Similar a la anterior, pero con nombre más descriptivo
    df['duracion_real'] = (df['completado_en'] - df['fecha_creacion']).dt.days
    print(f"Columna 'duracion_real' creada: {df['duracion_real']}")
    
    # COLUMNA DE CUMPLIMIENTO
    # Verificamos si la tarea se completó antes o en la fecha límite
    df['cumplimiento'] = df['completado_en'] <= df['fecha_limite']
    print(f"Columna 'cumplimiento' creada: {df['cumplimiento']}")
    
    # COLUMNA DE TIEMPO ESTIMADO EN HORAS
    # Convertimos minutos a horas para facilitar el análisis
    df['tiempo_estimado_horas'] = df['tiempo_estimado'] / 60
    print(f"Columna 'tiempo_estimado_horas' creada: {df['tiempo_estimado_horas']}")

def analizar_rendimiento():
    """
    PASO 5: ANÁLISIS DE RENDIMIENTO DEL EQUIPO
    Calculamos métricas clave para evaluar el desempeño
    """
    print("Analizando rendimiento del equipo...")

    # CÁLCULO DEL PORCENTAJE DE CUMPLIMIENTO
    # mean() en una columna booleana devuelve la proporción de True
    # Multiplicamos por 100 para obtener el porcentaje
    porcentaje_cumplimiento = df['cumplimiento'].mean() * 100
    print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")
    
    # CÁLCULO DE DÍAS DE RETRASO
    # Calculamos cuántos días de retraso tuvo cada tarea
    df['dias_retraso'] = (df['completado_en'] - df['fecha_limite']).dt.days
    retrasadas = df[df['dias_retraso'] > 0]
    print(f"Tareas entregadas fuera de plazo: {len(retrasadas)}")
    
    # ANÁLISIS DE RETRASOS
    if len(retrasadas) > 0:
        # Calculamos el promedio de días de retraso
        promedio_retraso = retrasadas['dias_retraso'].mean()
        print(f"Promedio de días de retraso: {promedio_retraso:.2f}")

def agrupar_por_prioridad():
    """
    PASO 6: ANÁLISIS AGRUPADO POR PRIORIDAD
    Analizamos cómo se comportan las tareas según su nivel de prioridad
    """
    print("Agrupando por prioridad...")
    
    # TIEMPO PROMEDIO ESTIMADO POR PRIORIDAD
    # groupby() agrupa los datos por la columna 'prioridad'
    # Luego calculamos la media del tiempo estimado para cada grupo
    tiempo_promedio = df.groupby('prioridad')['tiempo_estimado'].mean()
    print("Tiempo promedio estimado por prioridad:")
    print(tiempo_promedio)
    
    # ANÁLISIS DE TAREAS COMPLETADAS POR PRIORIDAD
    # Filtramos solo las tareas que tienen fecha de completado (no nula)
    completadas = df[df['completado_en'].notnull()]
    # Contamos cuántas tareas completadas hay por cada prioridad
    completadas_por_prioridad = completadas.groupby('prioridad').size()
    print("Tareas completadas por prioridad:")
    print(completadas_por_prioridad)

def analizar_por_mes():
    """
    PASO 7: ANÁLISIS TEMPORAL POR MES
    Analizamos la distribución de tareas por mes de creación
    """
    print("Analizando por mes de creación...")
    # Agrupamos por la columna 'mes' y contamos cuántas tareas hay en cada mes
    tareas_por_mes = df.groupby('mes').size()
    print(f"Tareas creadas por mes: {tareas_por_mes}")

def analizar_por_semana():
    """
    PASO 8: ANÁLISIS TEMPORAL POR SEMANA
    Analizamos la distribución de tareas completadas por semana
    """
    print("Analizando por semana...")
    # Agrupamos por la columna 'semana' y contamos las tareas completadas
    tareas_por_semana = df.groupby('semana').size()
    print(f"Tareas completadas por semana: {tareas_por_semana}")
    
def estadisticas_descriptivas():
    """
    PASO 9: ESTADÍSTICAS DESCRIPTIVAS FINALES
    Calculamos métricas resumen para entender el comportamiento general
    """
    print("Calculando estadísticas descriptivas...")
    
    # DURACIÓN PROMEDIO DE TAREAS
    # Calculamos el tiempo promedio estimado para todas las tareas
    promedio_duracion = df['tiempo_estimado'].mean()
    print(f"Promedio de duración estimada: {promedio_duracion:.2f} minutos")
    
    # ANÁLISIS DE PRODUCTIVIDAD DIARIA
    # Agrupamos por fecha de creación para ver la productividad diaria
    tareas_por_dia = df.groupby(df['fecha_creacion'].dt.date).size()
    print(f"Tareas creadas por día (últimos 10 días): {tareas_por_dia.tail(5)}")
    
    # MÉTRICA DE CUMPLIMIENTO GENERAL
    # Calculamos el porcentaje general de cumplimiento de plazos
    porcentaje_cumplimiento = df['cumplimiento'].mean() * 100
    print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")

# EJECUCIÓN DEL FLUJO COMPLETO DE PROCESAMIENTO
# Ejecutamos todas las funciones en el orden correcto para procesar los datos

# Paso 1: Limpieza básica de datos
limpiar_datos_basicos()

# Paso 2: Detección de datos problemáticos
detectar_outliers()

# Paso 3: Creación de nuevas columnas calculadas
crear_columnas_derivadas()

# Paso 4: Análisis de rendimiento del equipo
analizar_rendimiento()

# Paso 5: Análisis agrupado por prioridad
agrupar_por_prioridad()

# Paso 6: Análisis temporal por mes
analizar_por_mes()

# Paso 7: Análisis temporal por semana
analizar_por_semana()

# Paso 8: Estadísticas descriptivas finales
estadisticas_descriptivas()