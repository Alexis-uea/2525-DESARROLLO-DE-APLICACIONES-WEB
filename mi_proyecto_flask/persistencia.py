import os
import json
import csv

# Obtener la ruta absoluta de la carpeta 'instance'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')

# Asegurarse que la carpeta 'instance' existe
os.makedirs(INSTANCE_FOLDER, exist_ok=True)

# Archivos con ruta completa dentro de 'instance'
TXT_FILE = os.path.join(INSTANCE_FOLDER, 'productos.txt')
JSON_FILE = os.path.join(INSTANCE_FOLDER, 'productos.json')
CSV_FILE = os.path.join(INSTANCE_FOLDER, 'productos.csv')

# --- TXT ---
def guardar_productos_txt(productos, archivo=TXT_FILE):
    with open(archivo, 'w', encoding='utf-8') as f:
        for p in productos:
            linea = f"{p['id']},{p['nombre']},{p['cantidad']},{p['precio']}\n"
            f.write(linea)

def leer_productos_txt(archivo=TXT_FILE):
    productos = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(',')
                if len(partes) == 4:
                    productos.append({
                        'id': int(partes[0]),
                        'nombre': partes[1],
                        'cantidad': int(partes[2]),
                        'precio': float(partes[3])
                    })
    except FileNotFoundError:
        pass
    return productos

# --- JSON ---
def guardar_productos_json(productos, archivo=JSON_FILE):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(productos, f, ensure_ascii=False, indent=4)

def leer_productos_json(archivo=JSON_FILE):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- CSV ---
def guardar_productos_csv(productos, archivo=CSV_FILE):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nombre', 'cantidad', 'precio'])
        writer.writeheader()
        writer.writerows(productos)

def leer_productos_csv(archivo=CSV_FILE):
    productos = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                productos.append({
                    'id': int(row['id']),
                    'nombre': row['nombre'],
                    'cantidad': int(row['cantidad']),
                    'precio': float(row['precio'])
                })
    except FileNotFoundError:
        pass
    return productos
