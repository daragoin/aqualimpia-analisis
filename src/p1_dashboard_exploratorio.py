"""
PREGUNTA 1 - Abordaje analitico de la problematica y dashboard exploratorio.
AquaLimpia S. A. Reutiliza las funciones del modulo funciones_analisis.py.
Ejecutar: python p1_dashboard_exploratorio.py
"""
from funciones_analisis import (
    cargar_datos, calcular_eficiencia, indicadores_por_planta,
    correlaciones_dbo_salida, generar_dashboard, LIMITE_DBO_SALIDA,
)

# 1. Carga del dataset oficial del caso
df = cargar_datos("dataset_set_A_aguas_residuales.xlsx")
df = calcular_eficiencia(df)
print("Registros:", df.shape[0], "| Columnas:", df.shape[1])
print("Periodo:", df["fecha_registro"].min().date(), "a", df["fecha_registro"].max().date())

# 2. Situacion general del cumplimiento normativo
print("\n--- Cumplimiento normativo del efluente ---")
print("Limite de DBO en la salida:", LIMITE_DBO_SALIDA, "mg/L")
print("Registros que cumplen :", int(df["cumplimiento_norma"].sum()))
print("Registros que incumplen:", int((1 - df["cumplimiento_norma"]).sum()))
print("Tasa de cumplimiento  :", round(df["cumplimiento_norma"].mean(), 3))

# 3. Desempeno por planta
print("\n--- Indicadores por planta ---")
print(indicadores_por_planta(df).to_string())

# 4. Que variables se asocian al DBO de salida
print("\n--- Correlacion de cada variable con el DBO de salida ---")
print(correlaciones_dbo_salida(df).to_string())

# 5. Dashboard exploratorio de cuatro paneles
ruta = generar_dashboard(df, "dashboard_aqualimpia.png")
print("\n[OK] Dashboard generado:", ruta)
