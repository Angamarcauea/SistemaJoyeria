from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import Joya
from persistencia import guardar_persistencia_multiple # Importamos desde tu nuevo archivo
import os
import json

app = Flask(__name__)

# Configuración de Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joyeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def mostrar_inventario():
    lista_joyas = Joya.query.all()
    return render_template('inventario.html', lista=lista_joyas)

@app.route('/producto_form', methods=['GET', 'POST'])
def formulario_producto():
    if request.method == 'POST':
        n = request.form['nombre']
        m = request.form['material']
        c = int(request.form['cantidad'])
        p = float(request.form['precio'])

        # Guardar en SQLite
        nueva = Joya(nombre=n, material=m, cantidad=c, precio=p)
        db.session.add(nueva)
        db.session.commit()

        # Guardar en Archivos (Persistencia)
        guardar_persistencia_multiple(n, m, c, p)

        return redirect(url_for('mostrar_inventario'))
    return render_template('producto_form.html')

# ESTA ES LA FUNCIÓN QUE CORRIGE TU ERROR 'BuildError'
@app.route('/datos')
def ver_datos_archivos():
    ruta = 'data/datos.json'
    items = []
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            try: items = json.load(f)
            except: items = []
    return render_template('datos.html', lista=items)

@app.route('/clientes')
def mostrar_clientes():
    return render_template('clientes.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/factura')
def ver_factura():
    return render_template('factura.html')

if __name__ == '__main__':
    app.run(debug=True)