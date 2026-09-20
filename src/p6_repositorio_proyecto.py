"""
PREGUNTA 6 - Preparacion del repositorio del proyecto para publicacion en GitHub.
Organiza los archivos del analisis en la estructura del repositorio, separando
datos, codigo, salidas y documentacion.
Ejecutar: python p6_repositorio_proyecto.py
"""
import os, shutil

REPO = "aqualimpia-analisis"
ESTRUCTURA = {
    "data":      ["dataset_set_A_aguas_residuales.xlsx"],
    "src":       ["funciones_analisis.py", "p1_dashboard_exploratorio.py",
                  "p2_flujo_reproducible.py", "p3_documentacion.py",
                  "p4_scripts_modulares.py", "p5_calidad_datos.py",
                  "p6_repositorio_proyecto.py"],
    "outputs":   ["dashboard_aqualimpia.png", "reporte_area_operaciones.xlsx",
                  "reporte_area_gestion_ambiental.xlsx",
                  "resultados_aqualimpia.joblib", "indicadores_aqualimpia.joblib"],
    "notebooks": [],
}

# Se reconstruye desde cero para que el resultado sea siempre el mismo
if os.path.exists(REPO):
    shutil.rmtree(REPO)

print("--- Construccion de la estructura del repositorio ---")
for carpeta, archivos in ESTRUCTURA.items():
    destino = os.path.join(REPO, carpeta)
    os.makedirs(destino, exist_ok=True)
    print(f"\n{REPO}/{carpeta}/")
    for archivo in archivos:
        if os.path.exists(archivo):
            shutil.copy(archivo, destino)
            print("   +", archivo)
        else:
            print("   ! no encontrado:", archivo)

# La documentacion va en la raiz: es lo primero que GitHub muestra
if os.path.exists("README.md"):
    shutil.copy("README.md", REPO)
    print(f"\n{REPO}/README.md")
    print("   + README.md (documentacion tecnica del proyecto)")

# .gitignore: evita versionar artefactos binarios regenerables
with open(os.path.join(REPO, ".gitignore"), "w", encoding="utf-8") as f:
    f.write("__pycache__/\n*.pyc\n.ipynb_checkpoints/\n")
print("   + .gitignore")

print("\n--- Arbol del repositorio ---")
for raiz, _, archivos in sorted(os.walk(REPO)):
    nivel = raiz.replace(REPO, "").count(os.sep)
    print("   " * nivel + os.path.basename(raiz) + "/")
    for a in sorted(archivos):
        print("   " * (nivel + 1) + a)

print("\n[OK] Repositorio preparado en la carpeta:", REPO)
print("Siguiente paso: crear el repositorio en github.com y subir esta carpeta.")
