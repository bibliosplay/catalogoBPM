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

def cargar_inventario_real():
    global BD_LIBROS
    BD_LIBROS = []
    if not os.path.exists(RUTA_CSV):
        print("⚠️ Archivo inventario.csv no encontrado.")
        return

    # Usamos codificación cp1252/latin1 que es la nativa de Windows (ANSI) para Chile
    with open(RUTA_CSV, mode="r", encoding="latin-1", errors="ignore") as f:
        lector = csv.reader(f, delimiter=';')
        try: 
            next(lector)  # Saltar la cabecera: N° Sistema;Titulo;Autor...
        except StopIteration: 
            return

        for fila in lector:
            # Tu archivo tiene exactamente 6 columnas
            if len(fila) < 3: 
                continue
            try:
                # Limpiar espacios fantasmas generados por los anchos fijos de Aleph
                titulo_crudo = fila[1].strip()
                autor_crudo = fila[2].strip()
                clasificacion = fila[4].strip() if len(fila) > 4 else ""
                coleccion = fila[5].strip() if len(fila) > 5 else ""

                # 1. Limpieza profunda del Título (quitar barras cruzadas '/' y comillas)
                titulo = re.sub(r'\s*/\s*.*$', '', titulo_crudo)
                titulo = titulo.replace('"', '').replace('.', '').strip()
                
                # 2. Limpieza del Autor (dar vuelta "Abalo, Milagros" a "Milagros Abalo")
                autor = autor_crudo.replace('"', '').replace('.', '').strip()
                autor = re.sub(r',\s*\d{4}-?.*$', '', autor) # Quita años como 1982-
                autor = re.sub(r'\s+(autor|autora|ilustradora|editora|compilador).*$', '', autor, flags=re.IGNORECASE)
                
                autor_mostrar = autor
                if "," in autor:
                    partes = autor.split(",")
                    if len(partes) >= 2:
                        autor_mostrar = f"{partes[1].strip()} {partes[0].strip()}"
                
                if not autor_mostrar or autor_mostrar.lower() == "autor no registrado":
                    autor_mostrar = "Autor Institucional / Desconocido"

                # 3. Rescatar el Año analizando los códigos de la estantería
                año = "S/A"
                buscar_año = re.findall(r'\b(19\d{2}|20\d{2})\b', titulo_crudo + " " + clasificacion)
                if buscar_año: 
                    año = buscar_año[-1]

                # 4. Asignar sección humana basada en el código de colección (ej: LITCH)
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
    print(f"✅ ¡Éxito total! {len(BD_LIBROS)} libros reales en línea.")

cargar_inventario_real()

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
