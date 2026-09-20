"""
PREGUNTA 2 - Flujo de trabajo reproducible para analizar el desempeno de las plantas.
Ejecuta el proceso completo de principio a fin y documenta su configuracion.
Ejecutar: python p2_flujo_reproducible.py
"""
import sys, platform
import pandas as pd, numpy as np, scipy, joblib, matplotlib, seaborn

from funciones_analisis import (
    cargar_datos, evaluar_calidad, calcular_eficiencia, indicadores_por_planta,
    exportar_reportes_por_area, guardar_resultados, generar_dashboard,
)

SEMILLA = 42
np.random.seed(SEMILLA)   # fija la aleatoriedad: el analisis es repetible

# ------------------------------------------------------------------
# Entorno de ejecucion: queda registrado para poder reproducir el analisis
# ------------------------------------------------------------------
print("--- Configuracion del entorno ---")
print("Python     :", platform.python_version())
print("pandas     :", pd.__version__)
print("numpy      :", np.__version__)
print("scipy      :", scipy.__version__)
print("joblib     :", joblib.__version__)
print("matplotlib :", matplotlib.__version__)
print("seaborn    :", seaborn.__version__)
print("Semilla    :", SEMILLA)

# ------------------------------------------------------------------
# Etapa 1. Ingesta
# ------------------------------------------------------------------
print("\n[Etapa 1] Ingesta de datos")
df = cargar_datos("dataset_set_A_aguas_residuales.xlsx")
print("   Registros cargados:", len(df))

# ------------------------------------------------------------------
# Etapa 2. Evaluacion de calidad (antes de analizar)
# ------------------------------------------------------------------
print("\n[Etapa 2] Evaluacion de la calidad de los datos")
calidad = evaluar_calidad(df)
print("   Valores faltantes:", calidad["valores_faltantes"],
      "| Duplicados:", calidad["filas_duplicadas"])

# ------------------------------------------------------------------
# Etapa 3. Transformacion
# ------------------------------------------------------------------
print("\n[Etapa 3] Transformacion: indicadores derivados")
df = calcular_eficiencia(df)
print("   Columnas agregadas: eficiencia_remocion_pct, energia_por_m3_kWh")

# ------------------------------------------------------------------
# Etapa 4. Analisis
# ------------------------------------------------------------------
print("\n[Etapa 4] Analisis agregado por planta")
resumen = indicadores_por_planta(df)
print(resumen.to_string())

# ------------------------------------------------------------------
# Etapa 5. Visualizacion
# ------------------------------------------------------------------
print("\n[Etapa 5] Visualizacion")
print("   Dashboard:", generar_dashboard(df, "dashboard_aqualimpia.png"))

# ------------------------------------------------------------------
# Etapa 6. Salidas para las areas de la empresa
# ------------------------------------------------------------------
print("\n[Etapa 6] Exportacion de archivos por area")
for archivo in exportar_reportes_por_area(df):
    print("   Generado:", archivo)

# ------------------------------------------------------------------
# Etapa 7. Persistencia de resultados
# ------------------------------------------------------------------
print("\n[Etapa 7] Persistencia con Joblib")
artefacto = guardar_resultados(
    {"calidad": calidad, "resumen_plantas": resumen, "semilla": SEMILLA},
    "resultados_aqualimpia.joblib")
print("   Artefacto:", artefacto)
print("\nFlujo completado. Ejecutar este script reproduce el analisis completo.")
