import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# Importaciones para Autenticación
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_llave_secreta_luxury_2026'  # Necesaria para sesiones y mensajes flash

# 1. CONFIGURACIÓN DE MYSQL (Ajustada a tu base 'joyeria_db' de XAMPP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3307/joyeria_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. CONFIGURACIÓN DE FLASK-LOGIN
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirige aquí si se intenta entrar a una ruta protegida


# --- MODELOS DE BASE DE DATOS ---

# Modelo de Usuario (Requerido por la tarea)
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Almacenada directamente según la instrucción


# Modelo de Joya (Tu inventario)
class Joya(db.Model):
    __tablename__ = 'joyas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    material = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# --- FUNCIÓN DE PERSISTENCIA (JSON) ---
def guardar_persistencia_multiple(n, m, c, p):
    ruta = 'data/datos.json'
    os.makedirs('data', exist_ok=True)
    nuevo_item = {"nombre": n, "material": m, "cantidad": c, "precio": p}
    items = []
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            try:
                items = json.load(f)
            except:
                items = []
    items.append(nuevo_item)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=4, ensure_ascii=False)


# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Buscamos al usuario en MySQL
        user = Usuario.query.filter_by(email=email, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Verifique su correo y contraseña.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('register'))

        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- RUTAS DEL SISTEMA (TODAS PROTEGIDAS CON @login_required) ---

@app.route('/')
@login_required
def index():
    return render_template('index.html', usuario=current_user.nombre)


@app.route('/inventario')
@login_required
def mostrar_inventario():
    lista_joyas = Joya.query.all()
    return render_template('inventario.html', lista=lista_joyas)


@app.route('/producto_form', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    if request.method == 'POST':
        n = request.form['nombre']
        m = request.form['material']
        c = int(request.form['cantidad'])
        p = float(request.form['precio'])

        # Guardar en MySQL
        nueva = Joya(nombre=n, material=m, cantidad=c, precio=p)
        db.session.add(nueva)
        db.session.commit()

        # Guardar en Archivos (Persistencia)
        guardar_persistencia_multiple(n, m, c, p)

        return redirect(url_for('mostrar_inventario'))
    return render_template('producto_form.html')


@app.route('/datos')
@login_required
def ver_datos_archivos():
    ruta = 'data/datos.json'
    items = []
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            try:
                items = json.load(f)
            except:
                items = []
    return render_template('datos.html', lista=items)


@app.route('/clientes')
@login_required
def mostrar_clientes():
    return render_template('clientes.html')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/contactos')
@login_required
def contactos():
    return render_template('contactos.html')


@app.route('/factura')
@login_required
def ver_factura():
    return render_template('factura.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas 'usuarios' y 'joyas' en tu MySQL de XAMPP
    app.run(debug=True)