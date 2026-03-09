import json
import csv
import os
from database import db


class Joya(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)


# ESTA ES LA FUNCIÓN QUE FALTA O TIENE OTRO NOMBRE
def guardar_persistencia_multiple(n, m, c, p):
    if not os.path.exists('data'):
        os.makedirs('data')

    datos_dict = {"nombre": n, "material": m, "cantidad": c, "precio": p}

    # Persistencia TXT
    with open('data/datos.txt', 'a', encoding='utf-8') as f:
        f.write(f"{n}, {m}, {c}, {p}\n")

    # Persistencia JSON
    json_path = 'data/datos.json'
    lista = []
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                lista = json.load(f)
            except:
                lista = []
    lista.append(datos_dict)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4)

    # Persistencia CSV
    with open('data/datos.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([n, m, c, p])