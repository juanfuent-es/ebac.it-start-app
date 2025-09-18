# Importamos las librerías necesarias para el análisis de datos
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

def explorar_datos():
    """
    PASO 2: EXPLORACIÓN INICIAL DE DATOS
    Esta función nos ayuda a entender la estructura y calidad de nuestros datos
    """
    print("\nEXPLORACIÓN DE DATOS")
    print("=" * 40)
    
    # Mostramos las primeras 5 filas del DataFrame
    # Esto nos da una idea de cómo se ven los datos
    print("\nPrimeras 5 filas:")
    print(df.head())
    
    # Verificamos los tipos de datos de cada columna
    # Es importante saber si las fechas son strings o datetime, etc.
    print("\nTipos de datos:")
    print(df.dtypes)
    
    # Contamos los valores nulos (missing values) en cada columna
    # Los valores nulos pueden causar problemas en el análisis
    print("\nValores nulos:")
    print(df.isnull().sum())

def limpiar_datos():
    """
    PASO 3: LIMPIEZA Y TRANSFORMACIÓN DE DATOS
    Convertimos los datos a los tipos correctos para poder analizarlos
    """
    print("\nLIMPIEZA DE DATOS")
    print("=" * 40)    
    
    # CONVERSIÓN DE FECHAS
    # Convertimos las columnas de fecha de string a datetime
    # errors='coerce' convierte valores inválidos a NaT (Not a Time)
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'], errors='coerce')
    df['fecha_limite'] = pd.to_datetime(df['fecha_actualizacion'], errors='coerce')
    df['fecha_limite'] = pd.to_datetime(df['fecha_limite'], errors='coerce')
    df['completado_en'] = pd.to_datetime(df['completado_en'], errors='coerce')
    
    # CONVERSIÓN DE NÚMEROS
    # Convertimos tiempo_estimado a numérico para poder hacer cálculos
    df['tiempo_estimado'] = pd.to_numeric(df['tiempo_estimado'], errors='coerce')
    
    # Mostramos los tipos de datos después de la conversión
    print("Tipos de datos después de la limpieza:")
    print(df.dtypes)

def analizar_estados():
    """
    PASO 4: ANÁLISIS DE ESTADOS DE LAS TAREAS
    Analizamos cómo están distribuidas las tareas según su estado
    """
    print("\nANÁLISIS DE ESTADOS")
    print("=" * 40)
    
    # Verificamos que la columna 'estado' existe antes de analizarla
    if 'estado' in df.columns:
        # Contamos cuántas tareas hay en cada estado
        estados = df['estado'].value_counts()
        print("Distribución de estados:")
        print(estados)
        
        # Calculamos los porcentajes para entender mejor la distribución
        print("\nPorcentajes:")
        print((estados / len(df) * 100).round(1))

def analizar_prioridades():
    """Analiza las prioridades de las tareas"""
    print("\nANÁLISIS DE PRIORIDADES")
    print("=" * 40)
    
    if 'prioridad' in df.columns:
        prioridades = df['prioridad'].value_counts()
        print("Distribución de prioridades:")
        print(prioridades)
        
        # Porcentajes
        print("\nPorcentajes:")
        print((prioridades / len(df) * 100).round(1))

def analizar_tiempo():
    """Analiza el tiempo estimado de las tareas"""
    print("\nANÁLISIS DE TIEMPO")
    print("=" * 40)
    print("Estadísticas del tiempo estimado:")
    print(df['tiempo_estimado'].describe())    
    # Clasificación por duración
    df['tiempo_estimado_horas'] = df['tiempo_estimado'] / 60  # Convertir minutos a horas

    cortas = df[df['tiempo_estimado_horas'] <= .5].shape[0]
    medianas = df[(df['tiempo_estimado_horas'] > .5) & (df['tiempo_estimado_horas'] <= 1)].shape[0]
    largas = df[df['tiempo_estimado_horas'] > 1].shape[0]
    
    print(f"\nClasificación por duración:")
    print(f"Tareas cortas (≤ media hora): {cortas}")
    print(f"Tareas medianas (media hora - 1 hora): {medianas}")
    print(f"Tareas largas (> 1 hora): {largas}")

def filtrar_prioridades(prioridad='alta'):
    """Demuestra cómo filtrar tareas"""
    print("\nFILTROS DE TAREAS")
    print("=" * 40)
    # Tareas de alta prioridad
    filtradas = df[df['prioridad'] == prioridad]
    print(f"Tareas con prioridad {prioridad}: {len(filtradas)}")
    if len(filtradas) > 0:
        print("\nTareas filtradas:")
        print(filtradas[['nombre', 'prioridad', 'fecha_limite']].head())

def filtrar_estados(estado='pendiente'):
    """Demuestra cómo filtrar tareas"""
    print("\nFILTROS DE TAREAS")
    print("=" * 40)
    # Tareas de alta prioridad
    filtradas = df[df['estado'] == estado]
    print(f"Tareas con estado {estado}: {len(filtradas)}")
    if len(filtradas) > 0:
        print("\nTareas filtradas:")
        print(filtradas[['nombre', 'estado', 'fecha_limite']].head())


explorar_datos()
limpiar_datos()
analizar_estados()
analizar_prioridades()
analizar_tiempo()
filtrar_prioridades('baja')
filtrar_estados('completada')

df.to_csv('tareas.csv', index=True, encoding='utf-8')