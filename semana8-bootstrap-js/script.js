// Alerta personalizada
document.getElementById('alertBtn').addEventListener('click', () => {
  alert('¡Gracias por visitar nuestra tienda!');
});

// Validación del formulario
document.getElementById('contactForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const nombre = document.getElementById('nombre');
  const correo = document.getElementById('correo');
  const mensaje = document.getElementById('mensaje');

  let esValido = true;

  [nombre, correo, mensaje].forEach((campo) => {
    if (!campo.value.trim()) {
      campo.classList.add('is-invalid');
      esValido = false;
    } else {
      campo.classList.remove('is-invalid');
    }
  });

  if (esValido) {
    alert('Formulario enviado correctamente.');
    this.reset();
  }
});
