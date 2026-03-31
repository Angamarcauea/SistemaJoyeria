from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    # Formato: mysql+pymysql://usuario:password@localhost/nombre_db
    # Cambia 'root' y 'tu_password' por tus credenciales de MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:adm123@localhost/joyerialuxury'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)