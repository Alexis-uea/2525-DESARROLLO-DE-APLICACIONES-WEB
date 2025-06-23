// Obtener referencias a elementos del DOM
const galeria = document.getElementById('gallery');
const botonAgregar = document.getElementById('add-image');
const botonEliminar = document.getElementById('delete-image');
const inputURL = document.getElementById('image-url');

// Variable para guardar la imagen seleccionada actualmente
let imagenSeleccionada = null;

// Evento: cuando se hace clic en "Agregar Imagen"
botonAgregar.addEventListener('click', () => {
  const url = inputURL.value.trim(); // Obtener la URL del input

  // Validación: no permitir URLs vacías
  if (url === '') {
    alert('Por favor, ingresa una URL válida.');
    return;
  }

  // Crear un nuevo elemento <img>
  const img = document.createElement('img');
  img.src = url;
  img.alt = 'Imagen agregada por el usuario';

  // Evento: al hacer clic en una imagen, se selecciona
  img.addEventListener('click', () => seleccionarImagen(img));

  // Agregar imagen a la galería
  galeria.appendChild(img);
  inputURL.value = ''; // Limpiar el input
});

// Función para seleccionar una imagen
function seleccionarImagen(img) {
  // Si ya hay una imagen seleccionada, se deselecciona
  if (imagenSeleccionada) {
    imagenSeleccionada.classList.remove('selected');
  }

  // Se marca la nueva imagen como seleccionada
  img.classList.add('selected');
  imagenSeleccionada = img;
}

// Evento: cuando se hace clic en "Eliminar Imagen Seleccionada"
botonEliminar.addEventListener('click', () => {
  if (imagenSeleccionada) {
    // Eliminar la imagen del DOM
    galeria.removeChild(imagenSeleccionada);
    imagenSeleccionada = null; // Limpiar la selección
  } else {
    alert('Primero selecciona una imagen para eliminar.');
  }
});

// Evento: eliminar con la tecla "Delete"
document.addEventListener('keydown', (e) => {
  if (e.key === 'Delete' && imagenSeleccionada) {
    galeria.removeChild(imagenSeleccionada);
    imagenSeleccionada = null;
  }
});
