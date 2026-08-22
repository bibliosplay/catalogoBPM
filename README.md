# Buscador · Biblioteca Pública del Maule

Interfaz de búsqueda moderna y amigable para el catálogo de la Biblioteca Pública del Maule, pensada para usarse desde el celular. Reemplaza la vista clásica de ALEPH ([bncatalogo.cl](http://www.bncatalogo.cl)) por tarjetas simples con búsqueda instantánea por título, autor o ID.

## ¿Cómo funciona?

El sitio es estático (HTML + CSV) y no depende del catálogo en vivo:

1. `datos.csv` contiene una exportación del catálogo con las columnas `autor`, `titulo`, `id`.
2. `index.html` carga ese CSV en el navegador del usuario y permite buscar en tiempo real.
3. Cada resultado enlaza a la ficha original en `bncatalogo.cl` para ver disponibilidad, sede y detalles completos.

No hay backend ni base de datos: todo corre en el navegador.

## Estructura del repositorio

```
.
├── index.html      # interfaz de búsqueda
├── datos.csv        # exportación del catálogo (autor, titulo, id)
└── README.md
```

## Actualizar el catálogo

Cuando el equipo de sistemas del SBP entregue una nueva exportación:

1. Reemplaza `datos.csv` por el archivo nuevo (misma cabecera: `autor,titulo,id`).
2. Haz commit y push.
3. Listo — no hay que tocar `index.html`.

> El CSV debe mantener las comillas en los campos que contienen comas (por ejemplo `"Wilde, Oscar"`), ya que el parseo respeta el formato CSV estándar.

## Publicar con GitHub Pages

1. Ve a **Settings → Pages** en este repositorio.
2. En "Source", selecciona la rama principal (`main`) y la carpeta raíz (`/`).
3. Guarda — GitHub entrega una URL pública en `https://<usuario>.github.io/<repositorio>/`.

No requiere servidor propio ni configuración adicional.

## Notas técnicas

- El parseo del CSV usa [PapaParse](https://www.papaparse.com/) para manejar correctamente los campos con comas entre comillas.
- Los resultados se muestran en páginas de 40 tarjetas para no sobrecargar la carga inicial en celulares con conexiones lentas.
- Todos los textos se escapan antes de insertarse en el HTML para evitar inyección de código desde el CSV.

## Origen de los datos

Los datos provienen del catálogo público del Sistema Nacional de Bibliotecas Públicas (SBP), disponible en [bncatalogo.cl](http://www.bncatalogo.cl). Este proyecto no reemplaza el catálogo oficial, solo ofrece una vía de búsqueda alternativa más simple para los usuarios de la Biblioteca Pública del Maule.
