Análisis del desempeño de plantas de tratamiento — AquaLimpia S. A.

Objetivo
Evaluar el desempeño operacional y ambiental de las tres plantas de tratamiento
de AquaLimpia S. A., identificar los factores asociados al incumplimiento
normativo del efluente y entregar evidencia analítica reproducible que respalde
los informes de cumplimiento ante organismos fiscalizadores.

Preguntas de investigación
¿Qué variables del proceso se asocian al nivel de DBO del efluente tratado?
¿Existen diferencias de desempeño entre las tres plantas de tratamiento?
¿Con qué frecuencia se incumple el límite normativo y bajo qué condiciones?
¿La calidad del conjunto de datos permite sostener conclusiones operacionales?

Datos
Archivo dataset_set_A_aguas_residuales.xlsx, con 200 registros
y 12 variables, correspondientes al período
2025-07-01 a 2025-10-28.
No presenta valores faltantes ni filas duplicadas.

Variable	Descripción
fecha_registro	Fecha de la medición
planta	Planta de tratamiento (Norte, Centro, Sur)
caudal_entrada_m3_d	Caudal de entrada en metros cúbicos por día
DBO_entrada_mg_L	Demanda biológica de oxígeno a la entrada
SST_entrada_mg_L	Sólidos suspendidos totales a la entrada
pH_entrada	pH del afluente
energia_aeracion_kWh	Consumo de energía en aireación
lodos_generados_kg_d	Lodos generados por día
DBO_salida_mg_L	Demanda biológica de oxígeno del efluente tratado
cumplimiento_norma	1 si el registro cumple la normativa, 0 si no
	Metodología
Carga del dataset y normalización del tipo de fecha.
Evaluación de la calidad de los datos previa al análisis.
Cálculo de indicadores derivados: eficiencia de remoción de DBO y consumo
   de energía por metro cúbico tratado.
Agregación de indicadores por planta.
Inferencia estadística con SciPy: intervalos de confianza y ANOVA.
Construcción de un dashboard exploratorio de cuatro paneles.
Exportación de archivos de salida diferenciados por área.
Persistencia de los resultados con Joblib.

Estructura del repositorio
aqualimpia-analisis/
├── data/          dataset de entrada
├── src/           módulo de funciones y scripts de análisis
├── outputs/       reportes por área, dashboard y artefactos
├── notebooks/     notebook principal del análisis
└── README.md      esta documentación

Librerías y configuración
Librería	Uso en el proyecto
pandas	Carga, agregación y exportación de datos tabulares
numpy	Cálculo vectorizado de indicadores y percentiles
scipy	Intervalos de confianza y análisis de varianza
joblib	Persistencia de resultados entre ejecuciones
matplotlib / seaborn	Construcción del dashboard exploratorio
openpyxl	Lectura y escritura de archivos Excel
	Semilla de aleatoriedad fijada en 42. El flujo completo se reproduce ejecutando
python p2_flujo_reproducible.py.

Resultados
La tasa de cumplimiento normativo es de 0.225: solo
  45 de 200 registros cumplen el límite.
La carga orgánica de entrada es el factor más asociado al DBO del efluente
  (correlación de 0,759 con el DBO de salida).
Las tres plantas presentan un desempeño estadísticamente equivalente
  (ANOVA sobre la eficiencia de remoción: p = 0,242).
La eficiencia media de remoción alcanza
  87.09 %, con poca dispersión entre plantas.

Indicadores por planta
planta	registros	caudal_medio_m3_d	DBO_entrada_media	DBO_salida_media	eficiencia_media_pct	energia_por_m3_kWh	lodos_medios_kg_d	tasa_cumplimiento
Planta Centro	75	5112.72	285.187	35.901	87.513	0.246	433.011	0.227
Planta Norte	71	5287.87	275.845	36.561	86.647	0.245	450.472	0.169
Planta Sur	54	4684.52	278.796	36.057	87.096	0.254	394.441	0.296
	Observaciones
El conjunto de datos no presenta problemas de completitud, pero sí limitaciones
de cobertura: los registros se distribuyen de forma desigual entre plantas y
meses, y no existe un identificador único de muestra que permita distinguir
mediciones repetidas del mismo día. Estas limitaciones se detallan en el
apartado de calidad de los datos del informe.

Archivos de salida
Archivo	Área destinataria
reporte_area_operaciones.xlsx	Operaciones
reporte_area_gestion_ambiental.xlsx	Gestión Ambiental
dashboard_aqualimpia.png	Ambas
resultados_aqualimpia.joblib	Reutilización analítica
