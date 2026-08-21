import os
import re
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Catálogo Digital - BPM Talca")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RUTA_CSV = "inventario.csv"
BD_LIBROS = []

def cargar_inventario_indestructible():
    global BD_LIBROS
    BD_LIBROS = []
    if not os.path.exists(RUTA_CSV):
        return

    # Leemos línea por línea de forma directa para evitar errores de codificación con caracteres como N°
    with open(RUTA_CSV, mode="r", encoding="latin-1", errors="ignore") as f:
        for num_linea, linea in enumerate(f):
            # Saltar la primera línea (Cabecera) de forma segura
            if num_linea == 0:
                continue
                
            # Limpiar saltos de línea y separar estrictamente por punto y coma
            fila = [col.strip() for col in linea.split(';')]
            
            # Tu archivo tiene exactamente entre 5 y 6 columnas (N° Sistema, Titulo, Autor, Código, Clasificación, Colección)
            if len(fila) < 3:
                continue
                
            try:
                titulo_crudo = fila[1]
                autor_crudo = fila[2]
                clasificacion = fila[4] if len(fila) > 4 else ""
                coleccion = fila[5] if len(fila) > 5 else ""

                # Si la fila está vacía en los campos clave, la saltamos
                if not titulo_crudo and not autor_crudo:
                    continue

                # 1. Limpieza del Título
                titulo = re.sub(r'\s*/\s*.*$', '', titulo_crudo).replace('"', '').strip()
                
                # 2. Limpieza del Autor
                autor = autor_crudo.replace('"', '').strip()
                autor = re.sub(r',\s*\d{4}-?.*$', '', autor)  # Quitar años como 1982-
                autor = re.sub(r'\s+(autor|autora|ilustradora|editora|compilador).*$', '', autor, flags=re.IGNORECASE)
                
                autor_mostrar = autor
                if "," in autor:
                    partes = autor.split(",")
                    if len(partes) >= 2:
                        autor_mostrar = f"{partes[1].strip()} {partes[0].strip()}"
                
                if not autor_mostrar or autor_mostrar.lower() == "autor no registrado":
                    autor_mostrar = "Autor de la obra"

                # 3. Rescatar el Año
                año = "S/A"
                buscar_año = re.findall(r'\b(19\d{2}|20\d{2})\b', titulo_crudo + " " + clasificacion)
                if buscar_año:
                    año = buscar_año[-1]

                # 4. Clasificación amable de la sección
                ubicacion = "Estante General"
                seccion_cod = coleccion.upper() if coleccion else clasificacion.upper()
                if "LITCH" in seccion_cod or "CH" in seccion_cod:
                    ubicacion = "Colección Local / Literatura Chilena"
                elif "LITGE" in seccion_cod:
                    ubicacion = "Literatura General"

                BD_LIBROS.append({
                    "titulo": titulo,
                    "autor": autor_mostrar,
                    "autor_norm": autor_mostrar.lower(),
                    "titulo_norm": titulo.lower(),
                    "año": año,
                    "ubicacion": f"BP. Talca - {ubicacion}",
                    "formato": "Libro Físico"
                })
            except Exception:
                continue
    print(f"✅ ¡Éxito total en la nube! {len(BD_LIBROS)} libros reales cargados.")

cargar_inventario_indestructible()

@app.get("/api/buscar")
def buscar_libros(q: str = Query(..., description="Texto a buscar")):
    palabras_busqueda = q.lower().strip().split()
    coincidencias = []
    if not palabras_busqueda:
        return {"status": "ok", "total_resultados": 0, "libros": []}

    for libro in BD_LIBROS:
        cumple_filtro = True
        texto_combinado = f"{libro['titulo_norm']} {libro['autor_norm']}"
        for palabra in palabras_busqueda:
            if palabra not in texto_combinado:
                cumple_filtro = False
                break
        if cumple_filtro:
            coincidencias.append(libro)
    return {"status": "ok", "total_resultados": len(coincidencias), "libros": coincidencias[:40]}

@app.get("/", response_class=HTMLResponse)
def entregar_interfaz():
    with open("index.html", mode="r", encoding="utf-8") as f:
        return f.read()
