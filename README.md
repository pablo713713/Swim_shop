# 🏊 Tienda Virtual de Material de Natación

Este proyecto es una tienda en línea desarrollada para una empresa que vende material de natación. Permite a los clientes navegar por diferentes categorías de productos, aplicar filtros, ver imágenes de los artículos por color, añadir productos al carrito y realizar una compra simulada.

---
🏁 Instrucciones para iniciar el proyecto por primera vez
1. ✅ Requisitos
Tener MongoDB instalado.

Tener Mongo Shell (mongosh) o usarlo desde el terminal que instala MongoDB.


2. 🗂️ Crear carpeta de datos (solo la primera vez en Windows)
MongoDB necesita una carpeta por defecto para guardar los datos. Abre PowerShell como administrador y ejecuta lo siguiente:

```
if (-Not (Test-Path "C:\data\db")) {
    New-Item -ItemType Directory -Path "C:\data\db" -Force
    Write-Output " Carpeta C:\data\db creada correctamente."
} else {
    Write-Output " La carpeta C:\data\db ya existe."
} 

```
3. 🚀 Iniciar MongoDB
Si instalaste MongoDB como servicio, ya estará corriendo.
Si no, ejecuta en una terminal:
```
mongod
```
Si no te permite es por que MongoDB no está en el PATH del sistema ó MongoDB no está instalado como servicio, asi que ejecuta el siguiente comando:
```
& "C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" --dbpath C:\data\db
```
4. 🧠 Insertar datos de ejemplo
Abre otra terminal y ejecuta:
```
mongosh
```
Luego, dentro del shell (donde dice test>), escribe:
```
use swim_shop
```
Y después pega este script para insertar los productos:

```
db.productos.insertMany([
  {
    nombre: "Gorra Speedo",
    descripcion: "Gorra de natación de silicona resistente.",
    precio: 20,
    categoria: "gorras",
    colores: ["azul", "negro"],
    imagenes: {
      azul: "/static/img/gorra_azul.jpeg",
      negro: "/static/img/gorra_negra.jpg"
    }
  },
  {
    nombre: "Gorra TYR",
    descripcion: "Gorra ligera de látex ideal para entrenamientos diarios.",
    precio: 10.5,
    categoria: "gorras",
    colores: ["blanco", "rosa"],
    imagenes: {
      blanco: "/static/img/gorra_blanca.jpg",
      rosa: "/static/img/gorra_rosa.jpg"
    }
  },
  {
    nombre: "Lentes Arena Cobra Ultra",
    descripcion: "Lentes de natación antivaho con protección UV.",
    precio: 25.5,
    categoria: "lentes",
    colores: ["verde", "negro"],
    imagenes: {
      verde: "/static/img/lentes_verdes.jpg",
      negro: "/static/img/lentes_negros.jpg"
    }
  },
  {
    nombre: "Lentes Speedo Fastskin",
    descripcion: "Lentes de competencia con ajuste ergonómico.",
    precio: 30,
    categoria: "lentes",
    colores: ["blanco", "celeste"],
    imagenes: {
      blanco: "/static/img/lentes_blancos.jpeg",
      celeste: "/static/img/lentes_celestes.jpg"
    }
  },
  {
    nombre: "Malla TYR Mujer",
    descripcion: "Malla deportiva para entrenamiento femenino.",
    precio: 45,
    categoria: "mallas",
    colores: ["azul", "verde"],
    imagenes: {
      azul: "/static/img/malla_azul_mujer.jpg",
      verde: "/static/img/malla_verde_mujer.jpeg"
    }
  },
  {
    nombre: "Malla Speedo Hombre",
    descripcion: "Malla tipo jammer para natación masculina.",
    precio: 48,
    categoria: "mallas",
    colores: ["negro", "gris"],
    imagenes: {
      negro: "/static/img/malla_negra_hombre.jpg",
      gris: "/static/img/malla_gris_hombre.jpeg"
    }
  },
  {
    nombre: "Paletas Entrenamiento TYR",
    descripcion: "Paletas para mejorar la técnica de brazada.",
    precio: 20,
    categoria: "paletas",
    colores: ["amarillo", "rojo"],
    imagenes: {
      amarillo: "/static/img/paletas_amarillas.jpg",
      rojo: "/static/img/paletas_rojas.jpeg"
    }
  }
]);

```
---
## 🛒 Funcionalidades

- Navegación por categorías: Gorras, Lentes, Mallas, Paletas.
- Visualización de productos con imagen, nombre, descripción, precio y colores disponibles.
- Cambio dinámico de imagen al seleccionar un color (si aplica).
- Filtros por:
  - Marca
  - Precio mínimo y máximo
  - Color
- Carrito de compras:
  - Visualización del producto seleccionado y total de compra.
- Simulación de pago con tarjeta de crédito:
  - Aprobación aleatoria con 80% de probabilidad.
  - Mensaje en verde si se aprueba y se vacía el carrito.
  - Mensaje en rojo si se rechaza (fondos insuficientes), con opción de intentar nuevamente.

---

## 🧪 Tecnologías Usadas

- **Backend**: Flask (Python)
- **Base de Datos**: MongoDB
- **Cliente de Base de Datos**: MongoDB Compass
- **Frontend**: HTML, CSS

---

---
## 📁 Estructura de la Base de Datos

**Nombre de la base de datos:** `swim_shop`  
**Colección:** `productos`  

