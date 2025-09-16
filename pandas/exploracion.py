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

def mostrar_columnas_seguro(dataframe, columnas_deseadas, titulo="Datos"):
    """Muestra columnas de forma segura, solo las que existen"""
    
    columnas_disponibles = [col for col in columnas_deseadas if col in dataframe.columns]
    if columnas_disponibles:
        print(f"\n{titulo}:")
        print(dataframe[columnas_disponibles].head())
    else:
        print(f"No hay columnas disponibles para mostrar en {titulo}")
        print(f"Columnas deseadas: {columnas_deseadas}")
        print(f"Columnas disponibles: {list(dataframe.columns)}")

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
    df['fecha_limite'] = pd.to_datetime(df['fecha_limite'], errors='coerce')
    df['completado_en'] = pd.to_datetime(df['completado_en'], errors='coerce')
    df['tiempo_estimado'] = pd.to_numeric(df['tiempo_estimado'], errors='coerce')

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
    
    if 'tiempo_estimado' in df.columns:
        print("Estadísticas del tiempo estimado:")
        print(df['tiempo_estimado'].describe())
        
        # Clasificación por duración
        cortas = df[df['tiempo_estimado'] <= 2].shape[0]
        medianas = df[(df['tiempo_estimado'] > 2) & (df['tiempo_estimado'] <= 8)].shape[0]
        largas = df[df['tiempo_estimado'] > 8].shape[0]
        
        print(f"\nClasificación por duración:")
        print(f"Tareas cortas (≤2h): {cortas}")
        print(f"Tareas medianas (2-8h): {medianas}")
        print(f"Tareas largas (>8h): {largas}")

def filtrar_tareas():
    """Demuestra cómo filtrar tareas"""
    print("\nFILTROS DE TAREAS")
    print("=" * 40)
    
    # Tareas de alta prioridad
    if 'prioridad' in df.columns:
        urgentes = df[df['prioridad'] == 'Alta']
        print(f"Tareas de alta prioridad: {len(urgentes)}")
        if len(urgentes) > 0:
            mostrar_columnas_seguro(urgentes, ['titulo', 'prioridad', 'fecha_limite'], "Tareas urgentes")
    
    # Tareas pendientes
    if 'estado' in df.columns:
        pendientes = df[df['estado'] == 'pendiente']
        print(f"\nTareas pendientes: {len(pendientes)}")
        if len(pendientes) > 0:
            mostrar_columnas_seguro(pendientes, ['titulo', 'estado', 'fecha_limite'], "Tareas pendientes")

def resumen_final():
    """Muestra un resumen final"""
    print("\nRESUMEN FINAL")
    print("=" * 40)
    
    print(f"Total de tareas: {len(df)}")
    
    if 'completado_en' in df.columns:
        completadas = df['completado_en'].notnull().sum()
        print(f"Tareas completadas: {completadas}")
        print(f"Porcentaje completado: {(completadas/len(df)*100):.1f}%")
    
    if 'prioridad' in df.columns:
        prioridad_mas_comun = df['prioridad'].mode().iloc[0] if not df['prioridad'].mode().empty else "N/A"
        print(f"Prioridad más común: {prioridad_mas_comun}")
    
    if 'tiempo_estimado' in df.columns:
        tiempo_promedio = df['tiempo_estimado'].mean()
        print(f"Tiempo promedio estimado: {tiempo_promedio:.1f} horas")

# explorar_datos()  # Paso 2: Explorar datos
# limpiar_datos()  # Paso 3: Limpiar datos
# analizar_estados()  # Paso 4: Analizar estados
# analizar_prioridades()  # Paso 5: Analizar prioridades
# analizar_tiempo()  # Paso 6: Analizar tiempo
# filtrar_tareas()  # Paso 7: Filtrar tareas
# resumen_final()  # Paso 8: Resumen final