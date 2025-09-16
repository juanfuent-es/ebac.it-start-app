import requests
import pandas as pd

# Paso 1: Cargar datos  
resp = requests.get("http://localhost:5000/api/tareas")
try:
    datos = resp.json()
    df = pd.DataFrame(datos)
    # Cargar datos desde la API
    print("Datos cargados correctamente")
    print(f"Total de tareas: {len(df)}")
    print(f"Columnas disponibles: {list(df.columns)}")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    print("Sugerencia: Asegúrate de que la aplicación Flask esté ejecutándose en localhost:5000")
    df = pd.DataFrame()

def explorar_datos():
    """Explora la estructura básica de los datos"""
    print("\nEXPLORACIÓN DE DATOS")
    print("=" * 40)
    # Primeras filas
    print("\nPrimeras 5 filas:")
    print(df.head())
    # Información de tipos
    print("\nTipos de datos:")
    print(df.dtypes)
    # Valores nulos
    print("\nValores nulos:")
    print(df.isnull().sum())

def limpiar_datos():
    """Limpia y transforma los datos"""
    print("\nLIMPIEZA DE DATOS")
    print("=" * 40)    
    # Convertir fechas
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'], errors='coerce')
    df['fecha_limite'] = pd.to_datetime(df['fecha_actualizacion'], errors='coerce')
    df['fecha_limite'] = pd.to_datetime(df['fecha_limite'], errors='coerce')
    df['completado_en'] = pd.to_datetime(df['completado_en'], errors='coerce')
    df['tiempo_estimado'] = pd.to_numeric(df['tiempo_estimado'], errors='coerce')
    print(df.dtypes)

def analizar_estados():
    """Analiza los estados de las tareas"""
    print("\nANÁLISIS DE ESTADOS")
    print("=" * 40)
    
    if 'estado' in df.columns:
        estados = df['estado'].value_counts()
        print("Distribución de estados:")
        print(estados)
        
        # Porcentajes
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