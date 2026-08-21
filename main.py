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
        try:
            next(lector)  # Saltar cabecera
        except StopIteration:
            return

        for fila in lector:
            if len(fila) < 3:
                continue
            try:
                titulo_crudo = fila[1]
                autor_crudo = fila[2]
                clasificacion = fila[4] if len(fila) > 4 else ""

                titulo = re.sub(r'\s*/\s*.*$', '', titulo_crudo).replace('"', '').strip()
                autor = autor_crudo.replace('"', '').strip()
                autor = re.sub(r',\s*\d{4}-?.*$', '', autor)
                autor = re.sub(r'\s+(autor|autora|ilustradora|editora|compilador).*$', '', autor, flags=re.IGNORECASE)
                
                if "," in autor:
                    partes = autor.split(",")
                    autor = f"{partes[1].strip()} {partes[0].strip()}"
                if not autor or autor.lower() == "autor no registrado":
                    autor = "Autor de la obra"

                año = "S/A"
                buscar_año = re.findall(r'\b(19\d{2}|20\d{2})\b', titulo_crudo + " " + clasificacion)
                if buscar_año:
                    año = buscar_año[-1]

                BD_LIBROS.append({
                    "titulo": titulo,
                    "autor": autor,
                    "año": año,
                    "ubicacion": "Biblioteca Pública de Talca",
                    "formato": "Libro Físico"
                })
            except Exception:
                continue
    print(f"✅ Carga completa: {len(BD_LIBROS)} libros en línea.")

# Ejecutar de forma directa para producción en la nube
cargar_inventario_nube()

@app.get("/api/buscar")
def buscar_libros(q: str = Query(..., description="Texto a buscar")):
    palabra = q.lower().strip()
    coincidencias = []
    for libro in BD_LIBROS:
        if palabra in libro["titulo"].lower() or palabra in libro["autor"].lower():
            coincidencias.append(libro)
    return {"status": "ok", "total_resultados": len(coincidencias), "libros": coincidencias[:40]}

@app.get("/", response_class=HTMLResponse)
def entregar_interfaz():
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Móvil - BPM Talca</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background-color: #f8fafc; color: #1e293b; min-height: 100vh; display: flex; flex-direction: column; }
        header { background-color: #2563eb; color: white; padding: 1.2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        header h1 { font-size: 1.25rem; font-weight: 700; }
        .badge-online { background-color: #10b981; color: white; padding: 0.3rem 0.8rem; font-size: 0.72rem; font-weight: 600; border-radius: 50px; }
        main { flex: 1; max-width: 800px; width: 100%; margin: 0 auto; padding: 1.5rem; }
        .search-box { background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .search-box label { display: block; font-size: 0.9rem; font-weight: 600; color: #475569; margin-bottom: 0.6rem; }
        .form-group { display: flex; gap: 0.75rem; }
        input[type="text"] { flex: 1; padding: 0.75rem 1rem; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 0.75rem; font-size: 1rem; outline: none; }
        button { background-color: #2563eb; color: white; border: none; padding: 0.75rem 1.5rem; font-size: 1rem; font-weight: 600; border-radius: 0.75rem; cursor: pointer; }
        button:hover { background-color: #1d4ed8; }
        .state-container { text-align: center; padding: 3rem 1rem; color: #94a3b8; border: 2px dashed #e2e8f0; border-radius: 1rem; background-color: white; }
        .grid-results { display: grid; gap: 1rem; grid-template-columns: 1fr; }
        @media (min-width: 640px) { .grid-results { grid-template-columns: 1fr 1fr; } }
        .card { background: white; padding: 1.25rem; border-radius: 1rem; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; }
        .card-header { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.72rem; }
        .badge-format { background: #f1f5f9; color: #475569; padding: 0.2rem 0.5rem; border-radius: 0.4rem; font-weight: 600; }
        .badge-status { background: #ecfdf5; color: #065f46; padding: 0.2rem 0.5rem; border-radius: 0.4rem; font-weight: 600; }
        .card h3 { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 0.3rem; line-height: 1.4; }
        .card p { font-size: 0.88rem; color: #475569; font-weight: 500; }
        .card-footer { margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b; }
        .spinner { width: 2rem; height: 2rem; border: 4px solid #2563eb; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <header>
        <h1>Catálogo Digital</h1>
        <span class="badge-online">BPM Talca</span>
    </header>
    <main>
        <div class="search-box">
            <label for="search-input">Escribe el autor o título que buscas:</label>
            <form id="search-form" class="form-group">
                <input type="text" id="search-input-box" placeholder="Ej: Zurita, Bolaño, Allende..." required>
                <button type="submit">Buscar libro</button>
            </form>
        </div>
        <div id="loading-state" class="state-container hidden">
            <div class="spinner"></div>
            <p>Consultando las colecciones de la biblioteca...</p>
        </div>
        <div id="initial-state" class="state-container">
            <p>📖 Ingresa un término arriba para ver el resultado limpio en tarjetas.</p>
        </div>
        <div id="results-container" class="grid-results hidden"></div>
    </main>
    <script>
        const form = document.getElementById('search-form');
        const input = document.getElementById('search-input-box');
        const loadingState = document.getElementById('loading-state');
        const initialState = document.getElementById('initial-state');
        const resultsContainer = document.getElementById('results-container');

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const query = encodeURIComponent(input.value.trim());
            initialState.classList.add('hidden');
            resultsContainer.classList.add('hidden');
            loadingState.classList.remove('hidden');

            try {
                const respuesta = await fetch(`/api/buscar?q=${query}`);
                const datos = await respuesta.json();
                resultsContainer.innerHTML = '';
                loadingState.classList.add('hidden');
                resultsContainer.classList.remove('hidden');

                if (datos.status === "error" || !datos.libros || datos.libros.length === 0) {
                    resultsContainer.innerHTML = `<div class="state-container" style="grid-column: 1/-1; width:100%;"><p>🔍 No se encontraron registros para "${input.value}".</p></div>`;
                } else {
                    datos.libros.forEach(libro => {
                        const card = document.createElement('div');
                        card.className = "card";
                        card.innerHTML = `
                            <div>
                                <div class="card-header">
                                    <span class="badge-format">${libro.formato}</span>
                                    <span class="badge-status">Disponible</span>
                                </div>
                                <h3>${libro.titulo}</h3>
                                <p>${libro.autor}</p>
                            </div>
                            <div class="card-footer">
                                <span style="font-weight:600; color:#334155;">📍 ${libro.ubicacion}</span>
                                <span style="font-family:monospace;">${libro.año}</span>
                            </div>`;
                        resultsContainer.appendChild(card);
                    });
                }
            } catch (error) {
                loadingState.classList.add('hidden');
                resultsContainer.classList.remove('hidden');
                resultsContainer.innerHTML = `<div class="state-container" style="grid-column: 1/-1; color:#b91c1c;">⚠️ Error de conexión con el catálogo.</div>`;
            }
        });
    </script>
</body>
</html>"""
