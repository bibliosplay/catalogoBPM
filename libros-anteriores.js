// ARCHIVO DE LIBROS DESTACADOS ANTERIORES
// Este archivo NO se carga desde index.html. Es solo un respaldo de
// las selecciones que ya no estan en el carrusel, para reutilizarlas
// despues.
//
// Para reutilizar uno: copia el objeto al array `featuredBooks` de
// index.html y ajusta `semana` y `portada` (subiendo la imagen si ya
// no esta en el repo).

// Seleccion anterior a octubre (semanas 1 a 4).
const librosAnteriores = [
  {
    semana: 1,
    titulo: 'Diario de Japón',
    autor: 'María José Ferrada',
    rating: 3.97,
    resenas: 382,
    descripcion: 'Un libro híbrido entre diario de viajes, ensayo y crónica: Ferrada entreteje sus propios viajes a Tokio con una investigación sobre el Genji Monogatari y Murasaki Shikibu, la primera novelista de la historia, además de reflexiones sobre la escritura y la memoria. Reconocido con el Premio Manuel Montt.',
    tags: ['Ensayo autobiográfico', 'Crónica de viaje', 'Literatura chilena'],
    portada: 'portada-semana1.jpg'
  },
  {
    semana: 2,
    titulo: 'El Buzón de las Impuras',
    autor: 'Francisca Solar',
    rating: 4.70,
    resenas: 9900,
    descripcion: 'Novela histórica basada en el incendio de la Iglesia de la Compañía de 1863, donde murieron más de dos mil mujeres. A través de las Hijas de María, Solar denuncia la opresión femenina de la época: del fuego solo se salvó un buzón donde las asociadas confesaron sus más íntimos pecados.',
    tags: ['Novela histórica', 'Bestseller', 'Literatura chilena'],
    portada: 'portada-semana2.jpg'
  },
  {
    semana: 3,
    titulo: 'Una Promesa de Cien Años',
    autor: 'María Ignacia Urzúa Reyes',
    rating: 4.1,
    resenas: 500,
    descripcion: 'Debut literario de fantasía juvenil: hace cien años una guerra de división rompió la paz de Meliedor. Kal, un joven galduriano, encuentra a una sobreviviente sin recuerdos que lleva un símbolo prohibido, vestigio de la antigua alianza entre humanos y galdurianos.',
    tags: ['Fantasía', 'Juvenil', 'Debut literario'],
    portada: 'portada-semana3.jpg'
  },
  {
    semana: 4,
    titulo: 'Herbolario Mistraliano',
    autor: 'Gabriela Mistral',
    rating: 4.5,
    resenas: 120,
    descripcion: 'Homenaje al mundo vegetal y a los afectos naturales de la Premio Nobel: diarios y cuadernos de jardín que recopilan textos inéditos o ilocalizables de Gabriela Mistral, una faceta íntima de la poeta conectada con la naturaleza, las flores y la memoria.',
    tags: ['Diario', 'Naturaleza', 'Poesía chilena'],
    portada: 'portada-semana4.jpg'
  }
];

// Disponible en consola del navegador para inspeccionar el archivo:
//   console.table(librosAnteriores)