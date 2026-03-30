from flask_sqlalchemy import SQLAlchemy

# Creamos db aquí para que sea independiente
db = SQLAlchemy()

class Joya(db.Model):
    __tablename__ = 'joyas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    material = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)