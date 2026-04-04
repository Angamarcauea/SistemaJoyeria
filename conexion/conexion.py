import os

# Determinar la ruta absoluta de la base de datos para evitar errores de archivos no encontrados
basedir = os.path.abspath(os.path.dirname(__file__))

# 1. CONFIGURACIÓN DE LA CONEXIÓN
# Esto crea el archivo 'joyeria.db' dentro de la carpeta de tu proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'joyeria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. INICIALIZAR Y CREAR TABLAS
db.init_app(app)

with app.app_context():
    # Es vital importar los modelos aquí para que SQLAlchemy sepa qué tablas crear
    from models.joya import Joya

    # Si tienes más modelos en otros archivos, impórtalos aquí también

    db.create_all()
    print(f"Conexión establecida: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("Tablas creadas/verificadas en SQLite exitosamente.")