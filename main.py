import csv
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

def cargar_inventario_nube():
    global BD_LIBROS
    BD_LIBROS = []
    if not os.path.exists(RUTA_CSV):
        return

    with open(RUTA_CSV, mode="r", encoding="utf-8", errors="ignore") as f:
        lector = csv.reader(f, delimiter=';')
        try: next(lector)
        except StopIteration: return

        for fila in lector:
            if len(fila) < 3: continue
            try:
                # CORRECCIÓN TÉCNICA: Posicionamiento por índice de lista []
                titulo_crudo = fila[1] if len(fila) > 1 else ""
                autor_crudo = fila[2] if len(fila) > 2 else ""
                clasificacion = fila[4] if len(fila) > 4 else ""

                titulo = re.sub(r'\s*/\s*.*$', '', titulo_crudo).replace('"', '').strip()
                autor = autor_crudo.replace('"', '').strip()
                autor = re.sub(r',\s*\d{4}-?.*$', '', autor)
                autor = re.sub(r'\s+(autor|autora|ilustradora|editora|compilador).*$', '', autor, flags=re.IGNORECASE)
                
                autor_mostrar = autor
                if "," in autor:
                    partes = autor.split(",")
                    autor_mostrar = f"{partes[1].strip()} {partes[0].strip()}"
                
                if not autor_mostrar or autor_mostrar.lower() == "autor no registrado":
                    autor_mostrar = "Autor de la obra"

                año = "S/A"
                buscar_año = re.findall(r'\b(19\d{2}|20\d{2})\b', titulo_crudo + " " + clasificacion)
                if buscar_año: año = buscar_año[-1]

                BD_LIBROS.append({
                    "titulo": titulo,
                    "autor": autor_mostrar,
                    "autor_norm": autor_mostrar.lower(),
                    "titulo_norm": titulo.lower(),
                    "año": año,
                    "ubicacion": "Biblioteca Pública de Talca",
                    "formato": "Libro Físico"
                })
            except Exception: continue

cargar_inventario_nube()

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
