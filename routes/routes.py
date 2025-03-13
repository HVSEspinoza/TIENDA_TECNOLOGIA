from flask import render_template, request, redirect, url_for
from models.models import db, Producto, Almacen, ArchivoProcesado
from utils.helpers import procesar_csv, obtener_tipo_cambio, calcular_precio_con_igv, cargar_csv_a_bd
import os

def init_routes(app):
    print("Registrando rutas...")
    almacenes = {
        "alm000": "Lima - Principal", "alm010": "Chiclayo", "alm011": "Trujillo",
        "alm020": "Arequipa", "alm021": "Arequipa-Compuplaza", "alm030": "Cusco",
        "alm050": "Huancayo", "alm060": "Juliaca", "alm070": "Tarapoto", "alm080": "Tacna"
    }

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
        cargar_csv_a_bd(file_path, almacen_id, db.session)
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
            df = procesar_csv(file_path)
            df.fillna({'GARANTIA': 'sin_garantia', 'MARCA': 'sin_marca', 'CODIGO': 'sin_codigo', 
                       'DESCRIPCION': 'sin_descripcion', 'CATEGORIA': 'sin_categoria', 
                       'DETALLE PROMOCION': ''}, inplace=True)
            vista_previa_data = df.head(5).to_dict(orient='records')
            for i, fila in enumerate(vista_previa_data):
                fila['row_class'] = 'row-even' if i % 2 == 0 else 'row-odd'
            available_columns = df.columns.tolist()
            return render_template('vista_previa.html', archivo=archivo, datos=vista_previa_data, columnas=available_columns)
        except Exception as e:
            print(f"Error al procesar {file_path}: {str(e)}")
            return f"Error al leer el archivo '{archivo}': {str(e)}", 500

    @app.route('/productos', methods=['GET', 'POST'])
    def get_productos():
        print("Solicitud recibida en /productos")
        if request.method == 'POST':
            almacen_id = request.form['almacen_id']
            productos = db.session.query(Producto, Almacen).join(Almacen, Producto.almacen_id == Almacen.id).filter(Producto.almacen_id == almacen_id).all()
        else:
            productos = []
        tipo_cambio = obtener_tipo_cambio()
        igv = 0.18

        # Calcular promocion_soles para cada producto
        productos_con_promocion = []
        for producto, almacen in productos:
            promocion_soles = None
            if producto.promocion:
                # Convertir Decimal a float para evitar el error
                promocion_dolares = float(producto.promocion)
                promocion_soles = round(promocion_dolares * tipo_cambio * (1 + igv), 2)
            productos_con_promocion.append((producto, almacen, promocion_soles))

        return render_template('productos.html', productos=productos_con_promocion, almacenes=almacenes, tipo_cambio=tipo_cambio, igv=igv)