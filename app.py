from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
import os
import unicodedata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://HARD:Araza159753@localhost/tienda_tecnologia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

almacenes = {
    "alm000": "Lima - Principal",
    "alm010": "Chiclayo",
    "alm011": "Trujillo",
    "alm020": "Arequipa",
    "alm021": "Arequipa-Compuplaza",
    "alm030": "Cusco",
    "alm050": "Huancayo",
    "alm060": "Juliaca",
    "alm070": "Tarapoto",
    "alm080": "Tacna"
}

class Almacen(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio_dolares = db.Column(db.Numeric(10, 2), nullable=False)
    precio_soles = db.Column(db.Numeric(10, 2), nullable=False)
    garantia = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    promocion = db.Column(db.Numeric(10, 2), nullable=True)
    detalle_promocion = db.Column(db.String(255), nullable=True)
    almacen_id = db.Column(db.String(100), db.ForeignKey('almacen.id'))

class ArchivoProcesado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    procesado = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('ver_archivos'))

@app.route('/archivos')
def ver_archivos():
    archivos = os.listdir(app.config['UPLOAD_FOLDER'])
    archivos_procesados = {ap.nombre: ap.procesado for ap in ArchivoProcesado.query.all()}
    return render_template('archivos.html', archivos=archivos, almacenes=almacenes, archivos_procesados=archivos_procesados)

@app.route('/procesar', methods=['POST'])
def procesar_archivo():
    archivo = request.form['archivo']
    almacen_id = request.form['almacen_id']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
    cargar_csv_a_bd(file_path, almacen_id)
    archivo_procesado = ArchivoProcesado.query.filter_by(nombre=archivo).first()
    if not archivo_procesado:
        archivo_procesado = ArchivoProcesado(nombre=archivo, procesado=True)
        db.session.add(archivo_procesado)
    else:
        archivo_procesado.procesado = True
    db.session.commit()
    return redirect(url_for('ver_archivos'))

@app.route('/borrar/<archivo>', methods=['POST'])
def borrar_archivo(archivo):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('ver_archivos'))

@app.route('/vista_previa/<archivo>')
def vista_previa(archivo):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
    try:
        custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
        required_columns = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA"]
        
        # Normalizar custom_header y required_columns
        custom_header_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                    for col in custom_header]
        required_columns_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                       for col in required_columns]
        
        print(f"Intentando leer {file_path}")
        df = pd.read_csv(file_path, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
        print(f"Columnas encontradas en el CSV: {df.columns.tolist()}")
        
        # Normalizar columnas del CSV
        normalized_columns = [unicodedata.normalize('NFKD', col.strip()).encode('ASCII', 'ignore').decode('ASCII').upper()
                             for col in df.columns]
        df.columns = normalized_columns
        print(f"Columnas normalizadas: {df.columns.tolist()}")
        
        # Verificar columnas disponibles
        available_columns = [col for col in custom_header_normalized if col in df.columns]
        print(f"Columnas disponibles que coinciden: {available_columns}")
        missing_required = [col for col in required_columns_normalized if col not in df.columns]
        if missing_required:
            raise ValueError(f"El CSV no contiene todas las columnas requeridas. Faltan: {missing_required}, Encontradas: {df.columns.tolist()}")

        # Usar las columnas normalizadas disponibles
        df = df[available_columns]
        print("Primeras 5 filas del DataFrame:")
        print(df.head())

        # Procesar STOCK
        def convertir_stock(valor):
            if pd.isna(valor) or str(valor).strip() == '':
                return 0
            if str(valor).strip() == '>20':
                return 20
            try:
                return int(float(valor))
            except (ValueError, TypeError):
                return 0
        
        df['STOCK'] = df['STOCK'].apply(convertir_stock)
        df['PRECIO DOLARES'] = df['PRECIO DOLARES'].apply(lambda x: float(x) if pd.notna(x) and str(x).strip() != '' else 0.0)
        
        if 'PROMOCION' in df.columns:
            df['PROMOCION'] = df['PROMOCION'].apply(lambda x: float(str(x).replace('$', '')) if pd.notna(x) and str(x).strip() != '' else None)
        
        df.fillna({'GARANTIA': 'sin_garantia', 'MARCA': 'sin_marca', 'CODIGO': 'sin_codigo', 
                   'DESCRIPCION': 'sin_descripcion', 'CATEGORIA': 'sin_categoria', 
                   'DETALLE PROMOCION': ''}, inplace=True)
        
        vista_previa_data = df.head(5).to_dict(orient='records')
        for i, fila in enumerate(vista_previa_data):
            fila['row_class'] = 'row-even' if i % 2 == 0 else 'row-odd'
        
        return render_template('vista_previa.html', archivo=archivo, datos=vista_previa_data, columnas=available_columns)
    except Exception as e:
        print(f"Error al procesar {file_path}: {str(e)}")
        return f"Error al leer el archivo '{archivo}': {str(e)}", 500

@app.route('/productos', methods=['GET', 'POST'])
def get_productos():
    if request.method == 'POST':
        almacen_id = request.form['almacen_id']
        productos = db.session.query(Producto, Almacen).join(Almacen, Producto.almacen_id == Almacen.id).filter(Producto.almacen_id == almacen_id).all()
    else:
        productos = []
    tipo_cambio = obtener_tipo_cambio()
    igv = 0.18
    return render_template('productos.html', productos=productos, almacenes=almacenes, tipo_cambio=tipo_cambio, igv=igv)

def obtener_tipo_cambio():
    return 3.85

def calcular_precio_con_igv(precio_dolares, tipo_cambio, igv):
    precio_soles = precio_dolares * tipo_cambio
    precio_soles_con_igv = precio_soles * (1 + igv)
    return precio_soles_con_igv

def cargar_csv_a_bd(csv_file, almacen_id):
    custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
    required_columns = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA"]
    
    # Normalizar custom_header y required_columns
    custom_header_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                for col in custom_header]
    required_columns_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                   for col in required_columns]
    
    try:
        print(f"Procesando archivo: {csv_file}")
        data = pd.read_csv(csv_file, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
        print("Columnas en el CSV:", data.columns.tolist())
        
        # Normalizar columnas del CSV
        normalized_columns = [unicodedata.normalize('NFKD', col.strip()).encode('ASCII', 'ignore').decode('ASCII').upper()
                             for col in data.columns]
        data.columns = normalized_columns
        print(f"Columnas normalizadas: {data.columns.tolist()}")

        # Verificar columnas requeridas
        available_columns = [col for col in custom_header_normalized if col in data.columns]
        missing_required = [col for col in required_columns_normalized if col not in data.columns]
        if missing_required:
            print(f"El CSV no contiene todas las columnas requeridas: {missing_required}")
            return
        data = data[available_columns]

        # Conversiones
        def convertir_stock(valor):
            if pd.isna(valor) or str(valor).strip() == '':
                return 0
            if str(valor).strip() == '>20':
                return 20
            try:
                return int(float(valor))
            except (ValueError, TypeError):
                return 0

        def convertir_precio(valor):
            try:
                return float(str(valor).replace('$', '')) if pd.notna(valor) and str(valor).strip() != '' else 0.0
            except (ValueError, TypeError):
                return 0.0

        def convertir_texto(valor, max_length=255):
            texto = str(valor) if pd.notna(valor) and str(valor).strip() != '' else 'sin_valor'
            return texto[:max_length]

        data['STOCK'] = data['STOCK'].apply(convertir_stock)
        data['PRECIO DOLARES'] = data['PRECIO DOLARES'].apply(convertir_precio)
        if 'PROMOCION' in data.columns:
            data['PROMOCION'] = data['PROMOCION'].apply(convertir_precio)
        data['CODIGO'] = data['CODIGO'].apply(convertir_texto)
        data['DESCRIPCION'] = data['DESCRIPCION'].apply(lambda x: convertir_texto(x, 255))
        data['GARANTIA'] = data['GARANTIA'].apply(convertir_texto)
        data['MARCA'] = data['MARCA'].apply(lambda x: convertir_texto(x, 255))
        data['CATEGORIA'] = data['CATEGORIA'].apply(lambda x: convertir_texto(x, 255))
        if 'DETALLE PROMOCION' in data.columns:
            data['DETALLE PROMOCION'] = data['DETALLE PROMOCION'].apply(lambda x: convertir_texto(x, 255))

        tipo_cambio = obtener_tipo_cambio()
        igv = 0.18

        Producto.query.filter_by(almacen_id=almacen_id).delete()
        for _, row in data.iterrows():
            print(f"Procesando fila: {row}")
            precio_soles_con_igv = calcular_precio_con_igv(row['PRECIO DOLARES'], tipo_cambio, igv)
            promocion_valor = row['PROMOCION'] if 'PROMOCION' in row else None
            detalle_promocion = row['DETALLE PROMOCION'] if 'DETALLE PROMOCION' in row else ''
            nuevo_producto = Producto(
                codigo=row['CODIGO'],
                descripcion=row['DESCRIPCION'],
                stock=row['STOCK'],
                precio_dolares=row['PRECIO DOLARES'],
                precio_soles=precio_soles_con_igv,
                garantia=row['GARANTIA'],
                marca=row['MARCA'],
                categoria=row['CATEGORIA'],
                promocion=promocion_valor,
                detalle_promocion=detalle_promocion,
                almacen_id=almacen_id
            )
            db.session.add(nuevo_producto)
        db.session.commit()
        print(f"Datos del archivo {csv_file} cargados correctamente en la base de datos.")
    except Exception as e:
        print(f"Error al procesar el archivo '{csv_file}': {e}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)