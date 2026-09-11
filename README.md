# Buscador · Biblioteca Pública del Maule

Interfaz de búsqueda moderna y amigable para el catálogo de la Biblioteca Pública del Maule, pensada para usarse desde el celular. Reemplaza la vista clásica de ALEPH ([bncatalogo.cl](http://www.bncatalogo.cl)) por tarjetas simples con búsqueda instantánea por título, autor o ID, e incorpora una sección de libros destacados y comentarios de la comunidad.

## ¿Cómo funciona?

El sitio es estático (HTML + CSV), con un único servicio externo (Supabase) para los comentarios:

1. `datos.csv` contiene una exportación del catálogo con las columnas `autor`, `titulo`, `id`.
2. `index.html` carga ese CSV en el navegador del usuario y permite buscar en tiempo real con [PapaParse](https://www.papaparse.com/).
3. Cada resultado enlaza a la ficha original en `bncatalogo.cl` para ver disponibilidad, sede y detalles completos.
4. Un carrusel de **"Libros del Mes"** destaca una selección semanal definida directamente en `index.html`.
5. Una sección de **comentarios/recomendaciones** permite a los usuarios dejar reseñas, guardadas en Supabase y moderadas manualmente antes de publicarse.

No hay backend propio: la búsqueda corre 100% en el navegador y los comentarios se guardan en Supabase (Postgres + API REST gestionada).

## Estructura del repositorio

```
.
├── index.html              # interfaz de búsqueda, carrusel de libros del mes y comentarios
├── datos.csv                # exportación del catálogo (autor, titulo, id)
├── portada-semana1.jpg      # portada del libro destacado, semana 1
├── portada-semana2.jpg      # portada del libro destacado, semana 2
├── portada-semana3.jpg      # portada del libro destacado, semana 3
├── portada-semana4.jpg      # portada del libro destacado, semana 4
├── portada-libro-mes.jpg    # (sin usar actualmente, ver "Posibles mejoras")
└── README.md
```

## Actualizar el catálogo

Cuando el equipo de sistemas del SBP entregue una nueva exportación:

1. Reemplaza `datos.csv` por el archivo nuevo (misma cabecera: `autor,titulo,id`).
2. Haz commit y push.
3. Listo — no hay que tocar `index.html`.

> El CSV debe mantener las comillas en los campos que contienen comas (por ejemplo `"Wilde, Oscar"`), ya que el parseo respeta el formato CSV estándar.

## Actualizar los "Libros del Mes"

El carrusel se define a mano en el array `featuredBooks`, dentro de `index.html` (bloque `LIBROS DEL MES - CARRUSEL`):

1. Edita título, autor, descripción, tags y el nombre del archivo de portada (`portada`) de cada semana.
2. Sube la imagen de portada correspondiente al repositorio (formato vertical, idealmente proporción libro ~2:3, ver nota de tamaño más abajo).
3. Haz commit y push.

> Las portadas se recortan automáticamente (`object-fit: cover`) para llenar el marco de 132×189px (112×160px en pantallas angostas), así que no es necesario que todas las imágenes tengan el mismo tamaño exacto — solo una proporción similar para que el recorte no corte texto o rostros importantes.

## Comentarios y recomendaciones (Supabase)

Los usuarios pueden dejar comentarios sin necesidad de cuenta. Se guardan en una tabla `comentarios` de Supabase con moderación manual:

- Columnas esperadas: `nombre`, `libro` (opcional), `comentario`, `aprobado` (booleano), `created_at`.
- Solo se muestran públicamente los comentarios con `aprobado = true`.
- La moderación se hace manualmente desde el **Table Editor** de Supabase, marcando `aprobado` en `true`.
- Como protección anti-spam básica, el formulario incluye un campo *honeypot* oculto: si un bot lo rellena, el envío se descarta en silencio.

La URL y la clave pública (`anon key`) de Supabase están en `index.html`, dentro del bloque `CONFIGURACIÓN SUPABASE`. Es normal que la `anon key` sea visible en el código del cliente — está pensada para eso —, pero **la seguridad real depende de las políticas de Row Level Security (RLS)** configuradas en Supabase. Se recomienda verificar que:

- Solo se permita `INSERT` público (no `SELECT`, `UPDATE` ni `DELETE`) en la tabla `comentarios`.
- El `SELECT` público esté filtrado a `aprobado = true` (o gestionado vía una vista).

## Publicar con GitHub Pages

1. Ve a **Settings → Pages** en este repositorio.
2. En "Source", selecciona la rama principal (`main`) y la carpeta raíz (`/`).
3. Guarda — GitHub entrega una URL pública en `https://<usuario>.github.io/<repositorio>/`.

No requiere servidor propio ni configuración adicional.

## Notas técnicas

- El parseo del CSV usa [PapaParse](https://www.papaparse.com/) para manejar correctamente los campos con comas entre comillas.
- Los resultados se muestran en páginas de 40 tarjetas para no sobrecargar la carga inicial en celulares con conexiones lentas.
- Todos los textos (CSV y comentarios de Supabase) se escapan antes de insertarse en el HTML para evitar inyección de código.
- Los enlaces a fichas de `bncatalogo.cl` se generan rellenando el `id` a 9 dígitos con ceros a la izquierda; si el `id` no es puramente numérico, se enlaza al buscador general del catálogo como respaldo.
- La búsqueda ignora tildes (por ejemplo, "nunez" encuentra "Núñez").

## Origen de los datos

Los datos provienen del catálogo público del Sistema Nacional de Bibliotecas Públicas (SBP), disponible en [bncatalogo.cl](http://www.bncatalogo.cl). Este proyecto no reemplaza el catálogo oficial, solo ofrece una vía de búsqueda alternativa más simple para los usuarios de la Biblioteca Pública del Maule.

## Posibles mejoras

- **`portada-libro-mes.jpg` sin usar**: este archivo no está referenciado en `index.html` (el carrusel usa `portada-semana1.jpg` a `portada-semana4.jpg`). Se puede eliminar del repo, o reutilizar como imagen de respaldo (`fallback`) cuando a un libro destacado le falte portada.
- **`rating` y `resenas` sin mostrar**: cada libro del array `featuredBooks` define `rating` y `resenas`, pero el carrusel no los renderiza. O se agregan al diseño (por ejemplo, una insignia "★ 4.7 · 9.900 reseñas") o se quitan del array para no mantener datos muertos.
- **Automatizar el carrusel**: hoy los "Libros del Mes" se editan a mano en el código. Si se actualiza seguido, podría moverse a un pequeño JSON/CSV aparte (como `datos.csv`) para que alguien sin conocimientos de HTML/JS pueda actualizarlo.
- **Paginación vs. scroll infinito**: el botón "Mostrar más resultados" funciona bien, pero para catálogos que sigan creciendo podría evaluarse scroll infinito con `IntersectionObserver`.
- **Formulario de comentarios**: no hay límite de envíos por usuario/IP más allá del honeypot. Si llega a haber spam, conviene sumar un CAPTCHA simple (p. ej. Cloudflare Turnstile) o una regla de Supabase Edge Function con rate limiting.
- **Accesibilidad del carrusel**: las flechas y puntos tienen `aria-label`, pero el auto-play (rotación cada 5s) no se pausa si el usuario tiene `prefers-reduced-motion` activado — vale la pena respetarlo.
