from flask_sqlalchemy import SQLAlchemy

# Creamos db aquí para que sea independiente
db = SQLAlchemy()


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    # Relación: Una categoría tiene muchas joyas
    joyas = db.relationship('Joya', backref='categoria_rel', lazy=True)


class Joya(db.Model):
    __tablename__ = 'joyas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

    # NUEVO: Relación con la tabla categorías (La tercera tabla relacionada)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)