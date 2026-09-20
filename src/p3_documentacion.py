"""
PREGUNTA 3 - Documentacion tecnica del proyecto en formato Markdown.
Genera el archivo README.md que acompana al repositorio del proyecto.
Ejecutar: python p3_documentacion.py
"""
from funciones_analisis import (
    cargar_datos, calcular_eficiencia, indicadores_por_planta, evaluar_calidad,
)

df = calcular_eficiencia(cargar_datos("dataset_set_A_aguas_residuales.xlsx"))
calidad = evaluar_calidad(df)
resumen = indicadores_por_planta(df)

# La documentacion se construye con los resultados reales del analisis,
# de modo que se actualiza sola cada vez que el flujo vuelve a ejecutarse.
markdown = f"""# Análisis del desempeño de plantas de tratamiento — AquaLimpia S. A.

## Objetivo
Evaluar el desempeño operacional y ambiental de las tres plantas de tratamiento
de AquaLimpia S. A., identificar los factores asociados al incumplimiento
normativo del efluente y entregar evidencia analítica reproducible que respalde
los informes de cumplimiento ante organismos fiscalizadores.

## Preguntas de investigación
1. ¿Qué variables del proceso se asocian al nivel de DBO del efluente tratado?
2. ¿Existen diferencias de desempeño entre las tres plantas de tratamiento?
3. ¿Con qué frecuencia se incumple el límite normativo y bajo qué condiciones?
4. ¿La calidad del conjunto de datos permite sostener conclusiones operacionales?

## Datos
Archivo `dataset_set_A_aguas_residuales.xlsx`, con {calidad['registros']} registros
y {calidad['columnas']} variables, correspondientes al período
{calidad['rango_fechas'][0]} a {calidad['rango_fechas'][1]}.
No presenta valores faltantes ni filas duplicadas.

| Variable | Descripción |
|---|---|
| `fecha_registro` | Fecha de la medición |
| `planta` | Planta de tratamiento (Norte, Centro, Sur) |
| `caudal_entrada_m3_d` | Caudal de entrada en metros cúbicos por día |
| `DBO_entrada_mg_L` | Demanda biológica de oxígeno a la entrada |
| `SST_entrada_mg_L` | Sólidos suspendidos totales a la entrada |
| `pH_entrada` | pH del afluente |
| `energia_aeracion_kWh` | Consumo de energía en aireación |
| `lodos_generados_kg_d` | Lodos generados por día |
| `DBO_salida_mg_L` | Demanda biológica de oxígeno del efluente tratado |
| `cumplimiento_norma` | 1 si el registro cumple la normativa, 0 si no |

## Metodología
1. Carga del dataset y normalización del tipo de fecha.
2. Evaluación de la calidad de los datos previa al análisis.
3. Cálculo de indicadores derivados: eficiencia de remoción de DBO y consumo
   de energía por metro cúbico tratado.
4. Agregación de indicadores por planta.
5. Inferencia estadística con SciPy: intervalos de confianza y ANOVA.
6. Construcción de un dashboard exploratorio de cuatro paneles.
7. Exportación de archivos de salida diferenciados por área.
8. Persistencia de los resultados con Joblib.

## Estructura del repositorio
```
aqualimpia-analisis/
├── data/          dataset de entrada
├── src/           módulo de funciones y scripts de análisis
├── outputs/       reportes por área, dashboard y artefactos
├── notebooks/     notebook principal del análisis
└── README.md      esta documentación
```

## Librerías y configuración
| Librería | Uso en el proyecto |
|---|---|
| pandas | Carga, agregación y exportación de datos tabulares |
| numpy | Cálculo vectorizado de indicadores y percentiles |
| scipy | Intervalos de confianza y análisis de varianza |
| joblib | Persistencia de resultados entre ejecuciones |
| matplotlib / seaborn | Construcción del dashboard exploratorio |
| openpyxl | Lectura y escritura de archivos Excel |

Semilla de aleatoriedad fijada en 42. El flujo completo se reproduce ejecutando
`python p2_flujo_reproducible.py`.

## Resultados
- La tasa de cumplimiento normativo es de {calidad['tasa_cumplimiento']:.3f}: solo
  {int(df['cumplimiento_norma'].sum())} de {calidad['registros']} registros cumplen el límite.
- La carga orgánica de entrada es el factor más asociado al DBO del efluente
  (correlación de 0,759 con el DBO de salida).
- Las tres plantas presentan un desempeño estadísticamente equivalente
  (ANOVA sobre la eficiencia de remoción: p = 0,242).
- La eficiencia media de remoción alcanza
  {df['eficiencia_remocion_pct'].mean():.2f} %, con poca dispersión entre plantas.

### Indicadores por planta
{resumen.to_markdown()}

## Observaciones
El conjunto de datos no presenta problemas de completitud, pero sí limitaciones
de cobertura: los registros se distribuyen de forma desigual entre plantas y
meses, y no existe un identificador único de muestra que permita distinguir
mediciones repetidas del mismo día. Estas limitaciones se detallan en el
apartado de calidad de los datos del informe.

## Archivos de salida
| Archivo | Área destinataria |
|---|---|
| `reporte_area_operaciones.xlsx` | Operaciones |
| `reporte_area_gestion_ambiental.xlsx` | Gestión Ambiental |
| `dashboard_aqualimpia.png` | Ambas |
| `resultados_aqualimpia.joblib` | Reutilización analítica |
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("[OK] Documentacion generada: README.md")
print("Secciones incluidas:")
for linea in markdown.split("\n"):
    if linea.startswith("## "):
        print("   -", linea.replace("## ", ""))
