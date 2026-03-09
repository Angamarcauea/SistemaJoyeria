import os
import json
import csv


def guardar_persistencia_multiple(n, m, c, p):
    if not os.path.exists('data'):
        os.makedirs('data')

    # TXT
    with open('data/datos.txt', 'a', encoding='utf-8') as f:
        f.write(f"{n}, {m}, {c}, {p}\n")

    # JSON
    json_path = 'data/datos.json'
    lista = []
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                lista = json.load(f)
            except:
                lista = []
    lista.append({"nombre": n, "material": m, "cantidad": c, "precio": p})
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4)

    # CSV
    with open('data/datos.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([n, m, c, p])