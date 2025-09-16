# 📊 Análisis de Tareas con Pandas

Este módulo proporciona funciones útiles para analizar datos de tareas usando Pandas, respondiendo preguntas importantes sobre productividad y patrones de trabajo.

## 🚀 Características

### 📈 Análisis Temporal
- **¿Cuándo se crean más tareas?** Identifica patrones por hora, día de la semana y mes
- **¿Cuándo suelen vencer?** Analiza distribución de fechas límite y vencimientos

### 🎯 Análisis de Prioridades  
- **¿Qué urgencias se atienden más?** Distribución y tasa de completitud por prioridad
- **Patrones de priorización** Cruza prioridades con estados y tiempos

### ⏱️ Análisis de Duración
- **¿Cuánto duran las tareas?** Estadísticas de tiempo estimado y real
- **Estimación vs realidad** Compara tiempos planificados con ejecutados

### ✅ Análisis de Completitud
- **¿Qué tareas se completan?** Tasas de completitud y patrones
- **¿Cuándo se completan?** Análisis temporal de finalizaciones

### 📊 Visualizaciones y Reportes
- Dashboards automáticos con gráficos
- Exportación a CSV con métricas derivadas
- Reportes ejecutivos con insights clave

## 🛠️ Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar manualmente las principales
pip install pandas numpy matplotlib seaborn requests
```

## 📋 Uso Rápido

### Ejemplo Básico
```python
from analisis_tareas import *

# Cargar datos desde la API
df = cargar_datos_tareas()

# Análisis individual
analisis_creacion_tareas(df)
analisis_prioridades(df) 
analisis_duracion(df)
analisis_completitud(df)
```

### Reporte Completo
```python
# Generar reporte completo con todas las métricas
reporte = generar_reporte_completo(df)

# Crear visualizaciones
crear_visualizaciones(df)

# Exportar datos analizados
exportar_analisis(df, 'mi_analisis.csv')
```

### Demo Interactiva
```python
# Ejecutar demo completa
python demo_analisis.py
```

## 📁 Estructura de Archivos

```
pandas/
├── analisis_tareas.py      # Funciones principales de análisis
├── demo_analisis.py        # Script de demostración
├── exploracion.py          # Script original (base)
├── requirements.txt        # Dependencias
└── README.md              # Esta documentación
```

## 🔧 Funciones Principales

### Carga de Datos
- `cargar_datos_tareas()` - Carga y enriquece datos desde la API

### Análisis Temporal
- `analisis_creacion_tareas(df)` - Patrones de creación
- `analisis_vencimientos(df)` - Análisis de fechas límite

### Análisis de Contenido  
- `analisis_prioridades(df)` - Distribución y eficiencia por prioridad
- `analisis_duracion(df)` - Estadísticas de tiempo y duración
- `analisis_completitud(df)` - Tasas y patrones de completitud

### Reportes y Visualización
- `generar_reporte_completo(df)` - Reporte ejecutivo completo
- `crear_visualizaciones(df)` - Dashboard con gráficos
- `exportar_analisis(df)` - Exportar datos enriquecidos

## 📊 Métricas Generadas

### Métricas Temporales
- Hora pico de creación de tareas
- Día de la semana más productivo  
- Distribución mensual de actividad
- Promedio de tareas por día

### Métricas de Eficiencia
- Tasa de completitud general y por prioridad
- Tiempo promedio de ejecución
- Porcentaje de tareas completadas a tiempo
- Identificación de cuellos de botella

### Métricas de Planificación
- Precisión de estimaciones de tiempo
- Distribución de plazos de entrega
- Patrones de vencimiento
- Análisis de retrasos

## 🎨 Visualizaciones Incluidas

1. **Distribución de Estados** - Gráfico de pastel con estados de tareas
2. **Tareas por Prioridad** - Gráfico de barras con distribución
3. **Tiempo Estimado** - Histograma de distribución de duraciones  
4. **Creación por Día** - Gráfico de barras con patrones semanales

## 🔄 Datos Simulados

Como el sistema actual solo tiene columnas básicas (`created_at`, `updated_at`, `estado`), el módulo simula datos adicionales para demostrar capacidades de análisis:

- **fecha_limite** - Fechas límite simuladas (1-30 días después de creación)
- **prioridad** - Prioridades aleatorias (baja, media, alta, urgente)  
- **tiempo_estimado** - Duración estimada en horas (distribución log-normal)
- **completado_en** - Fechas de completado para tareas finalizadas

> 💡 **Nota**: En un sistema real, estos datos vendrían directamente de la base de datos.

## 🚦 Casos de Uso

### Para Gestores de Proyecto
- Identificar patrones de productividad del equipo
- Optimizar asignación de recursos por horarios
- Detectar cuellos de botella en el flujo de trabajo

### Para Desarrolladores  
- Mejorar estimaciones de tiempo basadas en datos históricos
- Identificar tipos de tareas que generan más retrasos
- Optimizar procesos de priorización

### Para Analistas de Datos
- Crear dashboards de productividad
- Generar reportes automáticos periódicos
- Desarrollar modelos predictivos de completitud

## 🔧 Personalización

### Agregar Nuevas Métricas
```python
def mi_analisis_personalizado(df):
    # Tu lógica de análisis aquí
    return resultados
```

### Modificar Visualizaciones
```python
def mis_graficos_personalizados(df):
    # Crear gráficos específicos
    plt.figure(figsize=(12, 8))
    # Tu código de visualización
```

### Exportar a Otros Formatos
```python
# Excel
df.to_excel('analisis.xlsx', index=False)

# JSON  
df.to_json('analisis.json', orient='records')

# Base de datos
df.to_sql('analisis_tareas', conexion_db)
```

## 🐛 Solución de Problemas

### Error: No hay datos disponibles
- Verificar que el servidor Flask esté corriendo en `localhost:5000`
- Confirmar que hay tareas en la base de datos

### Error: Módulo no encontrado
```bash
pip install -r requirements.txt
```

### Error en visualizaciones
- Instalar dependencias de visualización: `pip install matplotlib seaborn`
- En sistemas sin GUI, usar backend no interactivo: `matplotlib.use('Agg')`

## 📈 Próximos Pasos

1. **Integrar con datos reales** - Conectar directamente a la base de datos
2. **Automatizar reportes** - Crear tareas programadas (cron, scheduler)
3. **Dashboard web** - Crear interfaz web con Flask/Dash
4. **Alertas inteligentes** - Notificaciones basadas en métricas
5. **Machine Learning** - Modelos predictivos de completitud y duración

## 🤝 Contribuir

¿Tienes ideas para mejorar el análisis? ¡Contribuye!

1. Agrega nuevas funciones de análisis
2. Mejora las visualizaciones existentes  
3. Optimiza el rendimiento para datasets grandes
4. Agrega tests unitarios
5. Mejora la documentación

---

**¡Disfruta analizando tus datos de tareas! 📊✨**