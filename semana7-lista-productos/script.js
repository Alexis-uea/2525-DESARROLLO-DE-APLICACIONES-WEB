// Arreglo base de productos
let productos = [
  {
    nombre: "Laptop",
    precio: 1500,
    descripcion: "Computadora portátil de alto rendimiento."
  },
  {
    nombre: "Auriculares",
    precio: 200,
    descripcion: "Auriculares inalámbricos con cancelación de ruido."
  },
  {
    nombre: "Mouse",
    precio: 50,
    descripcion: "Mouse ergonómico para trabajo y juego."
  }
];

// Referencias al DOM
const listaProductos = document.getElementById("lista-productos");
const botonAgregar = document.getElementById("agregar-producto");

// Función para renderizar los productos
function renderizarProductos() {
  // Limpiar lista antes de renderizar
  listaProductos.innerHTML = "";

  productos.forEach(producto => {
    const item = document.createElement("li");
    item.innerHTML = `
      <strong>${producto.nombre}</strong><br/>
      Precio: $${producto.precio}<br/>
      <em>${producto.descripcion}</em>
    `;
    listaProductos.appendChild(item);
  });
}

// Evento para agregar un nuevo producto
botonAgregar.addEventListener("click", () => {
  const nuevoProducto = {
    nombre: "Nuevo Producto",
    precio: 100,
    descripcion: "Descripción de ejemplo."
  };
  productos.push(nuevoProducto);
  renderizarProductos();
});

// Renderizar al cargar la página
renderizarProductos();
