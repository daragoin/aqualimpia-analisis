"""
PREGUNTA 4 - Reutilizacion de scripts y codigo modular.
Demuestra el uso del modulo externo funciones_analisis.py y de las librerias
NumPy, SciPy y Joblib sobre el caso de AquaLimpia S. A.
Ejecutar: python p4_scripts_modulares.py
"""
import numpy as np
from joblib import load

# Las funciones se importan desde un archivo externo: no se reescribe codigo.
from funciones_analisis import (
    cargar_datos, calcular_eficiencia, intervalo_confianza,
    comparar_plantas, guardar_resultados,
)

df = calcular_eficiencia(cargar_datos("dataset_set_A_aguas_residuales.xlsx"))

# ------------------------------------------------------------------
# NumPy: operaciones vectorizadas sobre los arreglos de datos
# ------------------------------------------------------------------
print("--- NumPy: indicadores del efluente ---")
dbo_salida = df["DBO_salida_mg_L"].to_numpy()
print("Media      :", round(float(np.mean(dbo_salida)), 2), "mg/L")
print("Mediana    :", round(float(np.median(dbo_salida)), 2), "mg/L")
print("Desv. est. :", round(float(np.std(dbo_salida, ddof=1)), 2), "mg/L")
print("Percentil 90:", round(float(np.percentile(dbo_salida, 90)), 2), "mg/L")
# np.where evita recorrer el arreglo con un bucle
sobre_limite = np.where(dbo_salida > 30, 1, 0)
print("Registros sobre el limite:", int(sobre_limite.sum()), "de", len(dbo_salida))

# ------------------------------------------------------------------
# SciPy: inferencia estadistica
# ------------------------------------------------------------------
print("\n--- SciPy: intervalo de confianza del 95% ---")
ic_dbo = intervalo_confianza(df["DBO_salida_mg_L"])
print("DBO de salida       :", ic_dbo)
ic_efic = intervalo_confianza(df["eficiencia_remocion_pct"])
print("Eficiencia de remocion:", ic_efic)

print("\n--- SciPy: ANOVA entre plantas ---")
print("Eficiencia :", comparar_plantas(df, "eficiencia_remocion_pct"))
print("DBO salida :", comparar_plantas(df, "DBO_salida_mg_L"))

# ------------------------------------------------------------------
# Joblib: persistencia y reutilizacion de resultados
# ------------------------------------------------------------------
print("\n--- Joblib: persistencia de artefactos ---")
artefacto = guardar_resultados(
    {"ic_dbo_salida": ic_dbo, "ic_eficiencia": ic_efic},
    "indicadores_aqualimpia.joblib")
print("Guardado en:", artefacto)
recuperado = load("indicadores_aqualimpia.joblib")
print("Recuperado :", list(recuperado.keys()))
print("Media del DBO recuperada:", recuperado["ic_dbo_salida"]["media"], "mg/L")
