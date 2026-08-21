# 📚 Catálogo Digital Móvil - Biblioteca Pública de Talca (catalogoBPM)

Este proyecto es una interfaz web moderna, intuitiva y 100% responsiva (adaptada para teléfonos celulares) diseñada para modernizar el acceso al inventario de libros de la biblioteca, mitigando la obsolescencia tecnológica de los OPAC tradicionales.

## 🚀 Características Principales
* **Mobile-First**: Diseñado específicamente para pantallas táctiles de smartphones, evitando la necesidad de hacer zoom.
* **Buscador Único**: Barra de búsqueda central simplificada para encontrar autores o títulos de manera inmediata.
* **Normalización Automática**: El backend en Python limpia automáticamente errores comunes del catálogo crudo (comillas, orden de apellidos, eliminación de años de nacimiento en los autores).
* **Velocidad de Respuesta**: Indexación en memoria que procesa miles de registros en menos de un segundo.

## 📁 Estructura del Repositorio
* `main.py`: Código central en Python que maneja el servidor web (FastAPI) y renderiza la interfaz visual amable.
* `inventario.csv`: Base de datos local en texto plano (separada por punto y coma `;`) con los libros reales de la biblioteca.
* `requirements.txt`: Listado de librerías necesarias para el despliegue automático en la nube.

## 🔄 Cómo actualizar los libros en el futuro (Para Funcionarios)
Cuando el inventario de la biblioteca cambie, cualquier funcionario técnico puede actualizar el catálogo siguiendo estos pasos:
1. Exporte el nuevo listado de libros desde el software de gestión en formato **CSV**.
2. Asegúrese de que el separador sea **punto y coma (`;`)** y que las columnas mantengan el orden: *N° Sistema; Título; Autor; Código de Barras; Clasificación; Colección*.
3. Renombre el archivo exactamente como `inventario.csv`.
4. Ingrese a este repositorio de GitHub, haga clic en `Add file` -> `Upload files` y arrastre el nuevo archivo.
5. Render detectará el cambio y actualizará el buscador web automáticamente en 2 minutos sin apagar el servicio.

---
*Desarrollado con fines de modernización digital e inclusión tecnológica comunitaria en la Región del Maule.*
