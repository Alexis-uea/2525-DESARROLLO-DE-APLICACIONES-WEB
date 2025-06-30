// Obtener referencias a los elementos del formulario
const form = document.getElementById('formulario');
const nombre = document.getElementById('nombre');
const correo = document.getElementById('correo');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm-password');
const edad = document.getElementById('edad');
const submit = document.getElementById('submit');
const exito = document.getElementById('exito');

// Referencias a los contenedores de mensajes de error
const errorNombre = document.getElementById('error-nombre');
const errorCorreo = document.getElementById('error-correo');
const errorPassword = document.getElementById('error-password');
const errorConfirm = document.getElementById('error-confirm-password');
const errorEdad = document.getElementById('error-edad');

// Validación del campo Nombre
function validarNombre() {
  if (nombre.value.trim().length < 3) {
    errorNombre.textContent = "El nombre debe tener al menos 3 caracteres.";
    return false;
  }
  errorNombre.textContent = "";
  return true;
}

// Validación del campo Correo Electrónico usando expresión regular
function validarCorreo() {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(correo.value.trim())) {
    errorCorreo.textContent = "Correo no válido.";
    return false;
  }
  errorCorreo.textContent = "";
  return true;
}

// Validación de la Contraseña (mínimo 8 caracteres, un número y un carácter especial)
function validarPassword() {
  const regex = /^(?=.*[0-9])(?=.*[\W_]).{8,}$/;
  if (!regex.test(password.value)) {
    errorPassword.textContent = "Mínimo 8 caracteres, 1 número y 1 carácter especial.";
    return false;
  }
  errorPassword.textContent = "";
  return true;
}

// Confirmar que ambas contraseñas coinciden
function validarConfirmPassword() {
  if (confirmPassword.value !== password.value) {
    errorConfirm.textContent = "Las contraseñas no coinciden.";
    return false;
  }
  errorConfirm.textContent = "";
  return true;
}

// Validar que la edad sea mayor o igual a 18
function validarEdad() {
  if (parseInt(edad.value) < 18 || isNaN(edad.value)) {
    errorEdad.textContent = "Debes tener al menos 18 años.";
    return false;
  }
  errorEdad.textContent = "";
  return true;
}

// Función que valida todos los campos y activa o desactiva el botón de envío
function validarFormulario() {
  const valid =
    validarNombre() &&
    validarCorreo() &&
    validarPassword() &&
    validarConfirmPassword() &&
    validarEdad();

  // Activar o desactivar el botón de envío según validez
  submit.disabled = !valid;
}

// Añadir escuchadores de eventos para validar en tiempo real
[nombre, correo, password, confirmPassword, edad].forEach(input =>
  input.addEventListener('input', validarFormulario)
);

// Manejar el evento de envío del formulario
form.addEventListener('submit', function (e) {
  e.preventDefault(); // Prevenir envío por defecto

  if (!submit.disabled) {
    exito.textContent = "Formulario enviado correctamente.";
    form.reset();         // Limpiar los campos
    submit.disabled = true; // Desactivar el botón de nuevo
  }
});
