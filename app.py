import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# --- IMPORTACIÓN DE TUS CAPAS ---
# Asegúrate de que estas carpetas y archivos existan en tu proyecto
from models.joya import db, Joya
from services.joya_service import JoyaService
from services.reporte_service import ReporteService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_llave_secreta_luxury_2026'

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS (CORREGIDO A SQLITE) ---
# Esto creará un archivo llamado 'joyeria.db' en la raíz de tu proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joyeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 2. INICIALIZAR LA BASE DE DATOS ---
db.init_app(app)


# --- 3. MODELOS ADICIONALES ---
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Crear las tablas automáticamente al iniciar
with app.app_context():
    db.create_all()
    print("¡Base de datos SQLite local conectada y tablas creadas!")

# --- 4. CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


# --- PERSISTENCIA JSON ---
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
        user = Usuario.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
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


# --- RUTAS DEL SISTEMA ---

@app.route('/')
@login_required
def index():
    return render_template('index.html', usuario=current_user.nombre)


@app.route('/inventario')
@login_required
def mostrar_productos():
    lista_joyas = JoyaService.listar_todo()
    return render_template('productos.html', lista=lista_joyas)


@app.route('/producto_form', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    if request.method == 'POST':
        n = request.form['nombre']
        m = request.form['material']
        c = int(request.form['cantidad'])
        p = float(request.form['precio'])

        JoyaService.crear_joya(n, m, c, p)
        guardar_persistencia_multiple(n, m, c, p)

        return redirect(url_for('mostrar_productos'))
    return render_template('producto_form.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_joya(id):
    joya = db.session.get(Joya, id)
    if not joya:
        flash("Joya no encontrada")
        return redirect(url_for('mostrar_productos'))

    if request.method == 'POST':
        joya.nombre = request.form['nombre']
        joya.material = request.form['material']
        joya.cantidad = int(request.form['cantidad'])
        joya.precio = float(request.form['precio'])
        db.session.commit()
        return redirect(url_for('mostrar_productos'))
    return render_template('producto_form.html', joya=joya)


@app.route('/eliminar/<int:id>')
@login_required
def eliminar_joya_ruta(id):
    joya = db.session.get(Joya, id)
    if joya:
        db.session.delete(joya)
        db.session.commit()
    return redirect(url_for('mostrar_productos'))


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


@app.route('/descargar_reporte')
@login_required
def descargar_reporte():
    joyas = JoyaService.listar_todo()
    ruta_pdf = ReporteService.generar_pdf(joyas)
    return send_file(ruta_pdf, as_attachment=True)


# Rutas simples restantes
@app.route('/clientes')
@login_required
def mostrar_clientes(): return render_template('clientes.html')


@app.route('/about')
@login_required
def about(): return render_template('about.html')


@app.route('/contactos')
@login_required
def contactos(): return render_template('contactos.html')


@app.route('/factura')
@login_required
def ver_factura(): return render_template('factura.html')


if __name__ == '__main__':
    app.run(debug=True)

