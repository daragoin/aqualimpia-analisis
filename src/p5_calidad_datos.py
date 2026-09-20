"""
PREGUNTA 5 - Evaluacion de la calidad de los datos y riesgos asociados.
Ejecutar: python p5_calidad_datos.py
"""
import pandas as pd
import numpy as np
from funciones_analisis import cargar_datos, evaluar_calidad, LIMITE_DBO_SALIDA

pd.set_option("display.width", 140)
df = cargar_datos("dataset_set_A_aguas_residuales.xlsx")

# ------------------------------------------------------------------
# 1. Diagnostico general con la funcion del modulo
# ------------------------------------------------------------------
print("--- Diagnostico de calidad ---")
for clave, valor in evaluar_calidad(df).items():
    print(f"{clave:<32}: {valor}")

# ------------------------------------------------------------------
# 2. Completitud y tipos de dato
# ------------------------------------------------------------------
print("\n--- Tipos de dato y valores no nulos ---")
print(pd.DataFrame({"tipo": df.dtypes.astype(str),
                    "no_nulos": df.notnull().sum(),
                    "nulos": df.isnull().sum()}).to_string())

# ------------------------------------------------------------------
# 3. Rangos observados frente a rangos plausibles del proceso
# ------------------------------------------------------------------
print("\n--- Rangos observados en las variables numericas ---")
print(df.describe().loc[["min", "max"]].round(2).to_string())

# ------------------------------------------------------------------
# 4. Cobertura temporal por planta: base desigual entre unidades
# ------------------------------------------------------------------
print("\n--- Registros por planta y mes ---")
print(pd.crosstab(df["planta"], df["fecha_registro"].dt.to_period("M").astype(str)).to_string())

# ------------------------------------------------------------------
# 5. Consistencia de la variable objetivo frente al limite normativo
# ------------------------------------------------------------------
bajo = df["DBO_salida_mg_L"] <= LIMITE_DBO_SALIDA
cumple = df["cumplimiento_norma"] == 1
print("\n--- Consistencia de cumplimiento_norma ---")
print("Cumplen y estan bajo el limite    :", int((cumple & bajo).sum()))
print("Cumplen pero superan el limite    :", int((cumple & ~bajo).sum()))
print("No cumplen y superan el limite    :", int((~cumple & ~bajo).sum()))
print("No cumplen pese a estar bajo limite:", int((~cumple & bajo).sum()))

# ------------------------------------------------------------------
# 6. Valores atipicos por rango intercuartilico
# ------------------------------------------------------------------
print("\n--- Valores atipicos (criterio IQR) ---")
for col in ["caudal_entrada_m3_d", "DBO_entrada_mg_L", "DBO_salida_mg_L",
            "energia_aeracion_kWh", "lodos_generados_kg_d"]:
    q1, q3 = np.percentile(df[col], [25, 75])
    iqr = q3 - q1
    inf, sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n = int(((df[col] < inf) | (df[col] > sup)).sum())
    print(f"{col:<24}: {n:>3} atipicos  (limites {inf:.1f} a {sup:.1f})")
