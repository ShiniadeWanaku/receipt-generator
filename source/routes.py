# Import the random module to generate random numbers
import random

# Import necessary functions and classes from Flask module
from flask import render_template, redirect, url_for, request

# Import the Flask application instance from the source module
from source import app

# Import data models from the source.models module
from source.models import datos_recibidos, productos

# Route for the index page (root URL)
@app.route('/', methods=['GET', 'POST'])
def index():  
    # Render the index.html template and pass datos_recibidos and productos to it
    return render_template('index.html', datos_recibidos=datos_recibidos, productos=productos)

# Route for adding a product
@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the value of the 'accion' field from the form
    accion = request.form['accion']
    
    # Check if the action is to add a product
    if accion == 'agregar':
        # Check if the request method is POST
        if request.method == 'POST':
            # Extract product data from the form
            cantidad_producto = int(request.form['cantidad_producto'])
            descripcion_producto = request.form['descripcion_producto']
            medidas_producto = request.form['medidas_producto']
            precio_unitario_producto = float(request.form['precio_unitario_producto'])
            descuento_producto = float(request.form['descuento_producto'])
            total_producto = (cantidad_producto * precio_unitario_producto) - descuento_producto

            # Create a dictionary with the product data
            nuevo_producto = {
                'indice': len(productos) + 1,
                'cantidad': cantidad_producto,
                'descripcion': descripcion_producto,
                'medidas': medidas_producto,
                'precio_unitario': precio_unitario_producto,
                'descuento': descuento_producto,
                'total': total_producto
            }

            # Add the product to the list of productos
            productos.append(nuevo_producto)

            # Redirect to the index page after adding the product
            return redirect(url_for('index'))
    
    # If the action is to clear the products list
    elif accion == 'limpiar':
        # Clear the productos list
        productos.clear()
        
        # Redirect to the index page after clearing the list
        return redirect(url_for('index'))

# Route for deleting a product
@app.route('/delete_product/<int:indice>', methods=['POST'])
def delete_product(indice):
    # Find the product with the specified index in the productos list and remove it
    for producto in productos:
        if producto['indice'] == indice:
            productos.remove(producto)
            break

    # Redirect to the index page after deleting the product
    return redirect(url_for('index'))

# Route for fulfilling form submissions
@app.route('/fulfill', methods=['POST'])
def fulfill():
    # Clear the datos_recibidos list
    datos_recibidos.clear()
    
    # Initialize total cost
    total = 0.0
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Extract form data
        fecha = request.form.get('fecha')
        recibe = request.form.get('recibe')
        recibido_de = request.form.get('recibido_de')
        direccion = request.form.get('direccion')
        forma_pago = request.form.get('forma_pago')
        referencia_pago = request.form.get('referencia_pago')

        # Create a dictionary with the form data
        nuevo_dato = {
            'fecha': fecha,
            'recibe': recibe,
            'recibido_de': recibido_de,
            'direccion': direccion,
            'forma_pago': forma_pago,
            'referencia_pago': referencia_pago
        }

        # Calculate total cost
        total_sin_descuento = sum(producto['total'] for producto in productos)
        descuento_total = sum(producto['descuento'] for producto in productos)
        total = total_sin_descuento - descuento_total

        # Add the form data to the datos_recibidos list
        datos_recibidos.append(nuevo_dato)

        # Determine the action specified in the form
        accion = request.form['action']

        # Render the appropriate template based on the action
        if accion == 'quote':
            return render_template('quote.html', datos_recibidos=datos_recibidos[0], productos=productos, total=total, total_sin_descuento=total_sin_descuento, descuento_total=descuento_total, folio=random.randint(4000, 6000))
        elif accion == 'receipt':
            return render_template('receipt.html', datos_recibidos=datos_recibidos[0], productos=productos, total=total, total_sin_descuento=total_sin_descuento, descuento_total=descuento_total, folio=random.randint(4000, 6000))