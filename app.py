from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import random
from bson.objectid import ObjectId  
app = Flask(__name__)
app.secret_key = "secreto_super_secreto"  


app.config["MONGO_URI"] = "mongodb://localhost:27017/swim_shop"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/categoria/<nombre_categoria>')
def mostrar_categoria(nombre_categoria):
    productos = mongo.db.productos.find({"categoria": nombre_categoria})
    return render_template('categoria.html', productos=productos, categoria=nombre_categoria.capitalize())

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    nombre_producto = request.form.get('nombre')
    precio = float(request.form.get('precio', 0))
    cantidad = int(request.form.get('cantidad', 1))

    if 'carrito' not in session:
        session['carrito'] = []

    session['carrito'].append({
        "nombre": nombre_producto,
        "cantidad": cantidad,
        "precio": precio
    })
    session.modified = True

    return redirect(url_for('home'))


@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    return render_template('carrito.html', carrito=carrito)

@app.route('/pagar', methods=['POST', 'GET'])
def pagar():
    resultado = random.choices(["exito", "fracaso"], weights=[80, 20])[0]

    if resultado == "exito":
        flash("¡Compra realizada con éxito! Gracias por tu compra.", "success")
        session.pop('carrito', None) 
    else:
        flash("Fondos insuficientes. Intente de nuevo.", "error")

    return redirect(url_for('ver_carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        numero_tarjeta = request.form.get('numero_tarjeta', '')
        codigo_seguridad = request.form.get('codigo_seguridad', '')
        errores = []

        if not numero_tarjeta.isdigit():
            errores.append("El número de tarjeta debe contener solo números.")
        if not (codigo_seguridad.isdigit() and len(codigo_seguridad) == 4):
            errores.append("El código de seguridad debe tener exactamente 4 números.")

        if errores:
            return render_template('checkout.html', errores=errores)
        else:
            # Si todo está bien, proceder al pago (redirigir a /pagar)
            return redirect(url_for('pagar'))

    return render_template('checkout.html')

@app.route('/eliminar_del_carrito', methods=['POST'])
def eliminar_del_carrito():
    nombre_producto = request.form.get('nombre')

    if 'carrito' in session:
        session['carrito'] = [item for item in session['carrito'] if item['nombre'] != nombre_producto]
        session.modified = True

    return redirect(url_for('ver_carrito'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/create', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')

        # Procesar colores
        colores_input = request.form.get('colores', '')
        colores = [color.strip() for color in colores_input.split(',') if color.strip()]

        # Procesar imágenes
        imagenes_input = request.form.get('imagenes', '')
        imagenes_urls = [url.strip() for url in imagenes_input.split(',') if url.strip()]
        
        imagenes = {}
        for i in range(len(colores)):
            if i < len(imagenes_urls):
                imagenes[colores[i]] = imagenes_urls[i]
            else:
                imagenes[colores[i]] = ""

        # Crear documento
        nuevo_producto = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "categoria": categoria,
            "colores": colores,
            "imagenes": imagenes
        }

        # Insertar en la colección productos
        mongo.db.productos.insert_one(nuevo_producto)

        flash("Producto creado exitosamente.", "success")
        return redirect(url_for('admin'))

    return render_template('create_product.html')



@app.route('/admin/update')
def listar_productos_para_actualizar():
    productos = mongo.db.productos.find()
    return render_template('update_product.html', productos=productos)


@app.route('/admin/update/<id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    producto = mongo.db.productos.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')

        colores_input = request.form.get('colores', '')
        colores = [color.strip() for color in colores_input.split(',') if color.strip()]

        imagenes_input = request.form.get('imagenes', '')
        imagenes_urls = [url.strip() for url in imagenes_input.split(',') if url.strip()]

        imagenes = {}
        for i in range(len(colores)):
            if i < len(imagenes_urls):
                imagenes[colores[i]] = imagenes_urls[i]
            else:
                imagenes[colores[i]] = ""

        mongo.db.productos.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,
                    "categoria": categoria,
                    "colores": colores,
                    "imagenes": imagenes
                }
            }
        )

        flash("Producto actualizado exitosamente.", "success")
        return redirect(url_for('listar_productos_para_actualizar'))

    return render_template('edit_product.html', producto=producto)

@app.route('/admin/delete')
def listar_productos_para_eliminar():
    productos = mongo.db.productos.find()
    return render_template('delete_product_list.html', productos=productos)

    
@app.route('/admin/delete/<id>', methods=['POST'])
def eliminar_producto(id):
    mongo.db.productos.delete_one({"_id": ObjectId(id)})
    flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for('listar_productos_para_eliminar'))


@app.route('/buscar', methods=['GET'])
def buscar_productos():
    # Recibir filtros desde la URL
    marca = request.args.get('marca', '').strip()
    precio_min = request.args.get('precio_min')
    precio_max = request.args.get('precio_max')
    color = request.args.get('color', '').strip()

    # Construir la consulta de MongoDB
    filtro = {}

    # Marca: se busca en el nombre del producto como palabra
    if marca:
        filtro["nombre"] = {"$regex": rf"\b{marca}\b", "$options": "i"}

    # Precio mínimo y máximo
    if precio_min or precio_max:
        filtro["precio"] = {}
        if precio_min:
            filtro["precio"]["$gte"] = float(precio_min)
        if precio_max:
            filtro["precio"]["$lte"] = float(precio_max)

    # Color dentro del array de colores
    if color:
        filtro["colores"] = color

    productos_filtrados = list(mongo.db.productos.find(filtro))

    # Obtener todas las marcas y colores para los select
    todos_productos = mongo.db.productos.find()
    marcas = set()
    colores = set()
    for p in todos_productos:
        palabras = p['nombre'].split()
        if len(palabras) >= 2:
            marcas.add(palabras[1])
        colores.update(p.get('colores', []))

    return render_template(
        'search_products.html',
        marcas=sorted(marcas),
        colores=sorted(colores),
        resultados=productos_filtrados
    )



if __name__ == '__main__':
    app.run(debug=True)
