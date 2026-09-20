"""
funciones_analisis.py
Módulo de funciones reutilizables para el proyecto analítico de AquaLimpia S. A.

Separa las tareas frecuentes del análisis (carga, evaluación de calidad, cálculo
de indicadores, pruebas estadísticas, exportación y visualización) en funciones
con entradas y salidas claras, de modo que puedan invocarse desde cualquier
script o notebook sin reescribir código.

Librerías: pandas, numpy, scipy, joblib, matplotlib, seaborn.
Autor: Daniel Gómez — Ciencia de Datos, Unidad 3.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")                      # backend sin ventana: guarda archivos
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from joblib import dump, load

# Límite normativo de DBO en el efluente tratado, en mg/L.
# Se declara como constante del módulo para no repetirlo en cada función.
LIMITE_DBO_SALIDA = 30.0


# ----------------------------------------------------------------------
# 1. Carga de datos
# ----------------------------------------------------------------------
def cargar_datos(ruta_archivo):
    """Carga el dataset de AquaLimpia y normaliza el tipo de la fecha.

    Parámetros
    ----------
    ruta_archivo : str
        Ruta al archivo Excel entregado por el sistema de la empresa.

    Retorna
    -------
    pandas.DataFrame
        Conjunto de datos con `fecha_registro` convertida a datetime.
    """
    df = pd.read_excel(ruta_archivo)
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    return df


# ----------------------------------------------------------------------
# 2. Evaluación de la calidad de los datos
# ----------------------------------------------------------------------
def evaluar_calidad(df):
    """Revisa completitud, duplicados, rangos y consistencia del conjunto.

    Retorna
    -------
    dict
        Diccionario con los indicadores de calidad detectados.
    """
    columnas_requeridas = [
        "fecha_registro", "planta", "caudal_entrada_m3_d", "DBO_entrada_mg_L",
        "SST_entrada_mg_L", "pH_entrada", "energia_aeracion_kWh",
        "lodos_generados_kg_d", "DBO_salida_mg_L", "cumplimiento_norma",
    ]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el dataset: {faltantes}")

    # Consistencia de la variable objetivo: ¿el cumplimiento se explica
    # por el límite normativo de DBO en la salida?
    bajo_limite = df["DBO_salida_mg_L"] <= LIMITE_DBO_SALIDA
    cumple = df["cumplimiento_norma"] == 1

    return {
        "registros": int(len(df)),
        "columnas": int(df.shape[1]),
        "valores_faltantes": int(df.isnull().sum().sum()),
        "filas_duplicadas": int(df.duplicated().sum()),
        "pares_fecha_planta_repetidos": int(df.duplicated(subset=["fecha_registro", "planta"]).sum()),
        "registros_por_planta": df["planta"].value_counts().to_dict(),
        "rango_fechas": (str(df["fecha_registro"].min().date()),
                         str(df["fecha_registro"].max().date())),
        "pH_fuera_de_rango_6_9": int(((df["pH_entrada"] < 6) | (df["pH_entrada"] > 9)).sum()),
        "valores_negativos": int((df.select_dtypes(include=np.number) < 0).sum().sum()),
        "cumple_con_DBO_sobre_limite": int((cumple & ~bajo_limite).sum()),
        "no_cumple_con_DBO_bajo_limite": int((~cumple & bajo_limite).sum()),
        "tasa_cumplimiento": round(float(df["cumplimiento_norma"].mean()), 4),
    }


# ----------------------------------------------------------------------
# 3. Cálculo de indicadores de proceso
# ----------------------------------------------------------------------
def calcular_eficiencia(df):
    """Agrega la eficiencia de remoción de DBO y el consumo unitario de energía.

    La eficiencia se calcula con NumPy como el porcentaje de carga orgánica
    removida entre la entrada y la salida del proceso.
    """
    df = df.copy()
    df["eficiencia_remocion_pct"] = np.round(
        (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"]) / df["DBO_entrada_mg_L"] * 100, 2)
    # kWh consumidos por cada metro cúbico tratado
    df["energia_por_m3_kWh"] = np.round(
        df["energia_aeracion_kWh"] / df["caudal_entrada_m3_d"], 4)
    return df


def indicadores_por_planta(df):
    """Resume el desempeño operacional y ambiental de cada planta."""
    return df.groupby("planta").agg(
        registros=("planta", "size"),
        caudal_medio_m3_d=("caudal_entrada_m3_d", "mean"),
        DBO_entrada_media=("DBO_entrada_mg_L", "mean"),
        DBO_salida_media=("DBO_salida_mg_L", "mean"),
        eficiencia_media_pct=("eficiencia_remocion_pct", "mean"),
        energia_por_m3_kWh=("energia_por_m3_kWh", "mean"),
        lodos_medios_kg_d=("lodos_generados_kg_d", "mean"),
        tasa_cumplimiento=("cumplimiento_norma", "mean"),
    ).round(3)


def intervalo_confianza(serie, confianza=0.95):
    """Calcula el intervalo de confianza de la media mediante SciPy.

    Usa la distribución t de Student, apropiada cuando se estima la media
    de una población con desviación estándar desconocida.
    """
    datos = np.asarray(serie, dtype=float)
    media = np.mean(datos)
    inferior, superior = stats.t.interval(
        confianza, df=len(datos) - 1, loc=media, scale=stats.sem(datos))
    return {
        "media": round(float(media), 3),
        "desv_estandar": round(float(np.std(datos, ddof=1)), 3),
        "ic_inferior": round(float(inferior), 3),
        "ic_superior": round(float(superior), 3),
        "confianza": confianza,
    }


def comparar_plantas(df, variable="eficiencia_remocion_pct"):
    """Contrasta si las plantas difieren en una variable mediante ANOVA.

    La hipótesis nula sostiene que las tres plantas tienen la misma media.
    Un valor p bajo (< 0,05) indica que al menos una difiere de las demás.
    """
    grupos = [g[variable].values for _, g in df.groupby("planta")]
    f, p = stats.f_oneway(*grupos)
    return {
        "variable": variable,
        "estadistico_F": round(float(f), 4),
        "valor_p": round(float(p), 4),
        "diferencia_significativa": bool(p < 0.05),
    }


def correlaciones_dbo_salida(df):
    """Entrega la correlación de cada variable numérica con el DBO de salida."""
    numericas = df.select_dtypes(include=np.number)
    return numericas.corr()["DBO_salida_mg_L"].drop("DBO_salida_mg_L").round(3).sort_values()


# ----------------------------------------------------------------------
# 4. Exportación de resultados
# ----------------------------------------------------------------------
def exportar_reportes_por_area(df, ruta_operaciones="reporte_area_operaciones.xlsx",
                               ruta_ambiental="reporte_area_gestion_ambiental.xlsx"):
    """Genera un archivo de salida para cada área de la empresa.

    Operaciones necesita las variables del proceso; Gestión Ambiental, las
    del efluente y su cumplimiento normativo.
    """
    df[["fecha_registro", "planta", "caudal_entrada_m3_d", "DBO_entrada_mg_L",
        "DBO_salida_mg_L", "energia_aeracion_kWh", "lodos_generados_kg_d",
        "eficiencia_remocion_pct", "energia_por_m3_kWh"]].to_excel(
            ruta_operaciones, index=False)

    df[["fecha_registro", "planta", "DBO_salida_mg_L",
        "cumplimiento_norma"]].to_excel(ruta_ambiental, index=False)

    return [ruta_operaciones, ruta_ambiental]


def guardar_resultados(objeto, ruta="resultados_aqualimpia.joblib"):
    """Persiste los resultados del análisis con Joblib para reutilizarlos."""
    dump(objeto, ruta)
    return ruta


def cargar_resultados(ruta="resultados_aqualimpia.joblib"):
    """Recupera resultados previamente guardados con Joblib."""
    return load(ruta)


# ----------------------------------------------------------------------
# 5. Visualización
# ----------------------------------------------------------------------
def generar_dashboard(df, ruta_salida="dashboard_aqualimpia.png"):
    """Construye un dashboard exploratorio de cuatro paneles.

    Cada panel responde una pregunta distinta sobre el desempeño de las
    plantas: cumplimiento, evolución, relación carga-salida y eficiencia.
    """
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(2, 2, figsize=(15, 9))

    # Panel 1: cumplimiento normativo por planta
    cumpl = df.groupby("planta")["cumplimiento_norma"].mean().sort_values()
    ax[0, 0].bar(cumpl.index, cumpl.values, color="#4C72B0")
    ax[0, 0].axhline(df["cumplimiento_norma"].mean(), color="gray", linestyle="--",
                     label=f"Promedio general ({df['cumplimiento_norma'].mean():.2f})")
    ax[0, 0].set_title("Tasa de cumplimiento normativo por planta")
    ax[0, 0].set_ylabel("Proporción de registros que cumplen")
    ax[0, 0].set_ylim(0, 0.5)
    ax[0, 0].legend()

    # Panel 2: evolución mensual del DBO de salida
    mensual = df.groupby([df["fecha_registro"].dt.to_period("M").astype(str), "planta"]
                         )["DBO_salida_mg_L"].mean().unstack()
    for planta in mensual.columns:
        ax[0, 1].plot(mensual.index, mensual[planta], marker="o", label=planta)
    ax[0, 1].axhline(LIMITE_DBO_SALIDA, color="red", linestyle="--",
                     label=f"Límite normativo ({LIMITE_DBO_SALIDA:.0f} mg/L)")
    ax[0, 1].set_title("DBO de salida promedio por mes")
    ax[0, 1].set_ylabel("DBO salida (mg/L)")
    ax[0, 1].set_xlabel("Mes")
    ax[0, 1].legend(fontsize=8)

    # Panel 3: relación entre carga de entrada y calidad del efluente
    sns.scatterplot(data=df, x="DBO_entrada_mg_L", y="DBO_salida_mg_L",
                    hue="planta", s=45, alpha=0.8, ax=ax[1, 0])
    ax[1, 0].axhline(LIMITE_DBO_SALIDA, color="red", linestyle="--")
    ax[1, 0].set_title("Carga de entrada frente a DBO de salida")
    ax[1, 0].set_xlabel("DBO entrada (mg/L)")
    ax[1, 0].set_ylabel("DBO salida (mg/L)")

    # Panel 4: distribución de la eficiencia de remoción
    sns.boxplot(data=df, x="planta", y="eficiencia_remocion_pct",
                hue="planta", legend=False, palette="Set2", ax=ax[1, 1])
    ax[1, 1].set_title("Eficiencia de remoción de DBO por planta")
    ax[1, 1].set_xlabel("Planta")
    ax[1, 1].set_ylabel("Eficiencia (%)")

    fig.suptitle("Dashboard exploratorio — Desempeño de plantas de AquaLimpia S. A.",
                 fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=140)
    plt.close()
    return ruta_salida
