from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from decimal import Decimal
from models.models import Almacen, Producto, db, ArchivoProcesado
from utils.helpers import obtener_tipo_cambio, recalcular_precios_en_soles, cargar_csv_a_bd, procesar_csv
import os
import pandas as pd
from collections import defaultdict
from models.models import Producto, db

# Definir el blueprint
routes = Blueprint('routes', __name__)

# Rutas usando el blueprint
@routes.route('/')
def index():
    almacenes = Almacen.query.all()
    return render_template('index.html', almacenes={almacen.id: almacen.nombre for almacen in almacenes})

@routes.route('/productos', methods=['GET', 'POST'])
def get_productos():
    tipo_cambio = obtener_tipo_cambio()
    igv = Decimal('0.18')

    # Siempre consultar todos los productos, luego filtrar si es necesario
    productos = Producto.query.all()

    if request.method == 'POST':
        almacen_id = request.form.get('almacen_id')
        if almacen_id and almacen_id != '':
            # Filtrar los productos unificados para mostrar solo los que tienen stock en el almacén seleccionado
            productos = [p for p in productos if p.almacen_id == almacen_id]

    # Unificar productos
    productos_unificados = defaultdict(lambda: {
        "id": None,
        "codigo": "",
        "descripcion": "",
        "stock": 0,
        "precio_compra_usd": Decimal('0.0'),
        "precio_compra_soles": Decimal('0.0'),
        "precio_oferta_compra_usd": None,
        "precio_oferta_compra_soles": None,
        "garantia": "",
        "marca": "",
        "categoria": "",
        "detalle_promocion": "",
        "stock_por_almacen": {}
    })

    for producto in productos:
        codigo = producto.codigo
        info = productos_unificados[codigo]

        # Asignar datos (tomamos el primero no vacío)
        if not info["id"]:
            info["id"] = producto.id
        info["codigo"] = producto.codigo or info["codigo"]
        info["descripcion"] = producto.descripcion or info["descripcion"]
        info["garantia"] = producto.garantia or info["garantia"]
        info["marca"] = producto.marca or info["marca"]
        info["categoria"] = producto.categoria or info["categoria"]
        info["detalle_promocion"] = producto.detalle_promocion or info["detalle_promocion"]
        if info["precio_compra_usd"] == Decimal('0.0'):
            info["precio_compra_usd"] = producto.precio_compra_usd
        if info["precio_compra_soles"] == Decimal('0.0'):
            info["precio_compra_soles"] = producto.precio_compra_soles
        if info["precio_oferta_compra_usd"] is None and producto.precio_oferta_compra_usd is not None:
            info["precio_oferta_compra_usd"] = producto.precio_oferta_compra_usd
        if info["precio_oferta_compra_soles"] is None and producto.precio_oferta_compra_soles is not None:
            info["precio_oferta_compra_soles"] = producto.precio_oferta_compra_soles

        # Sumar stock y registrar por almacén
        stock = int(producto.stock or 0)
        info["stock"] += stock
        almacen_nombre = producto.almacen.nombre if producto.almacen else "Desconocido"
        if stock > 0:
            info["stock_por_almacen"][almacen_nombre] = info["stock_por_almacen"].get(almacen_nombre, 0) + stock

    # Convertir a lista y preparar datos para la plantilla
    productos_con_detalles = []
    utilidad_bruta_total = Decimal('0')
    utilidad_neta_total = Decimal('0')

    for codigo, info in productos_unificados.items():
        if info["stock"] > 0:
            class ProductoUnificado:
                def __init__(self, info):
                    self.id = info["id"]
                    self.codigo = info["codigo"]
                    self.descripcion = info["descripcion"]
                    self.stock = info["stock"]
                    self.precio_compra_usd = info["precio_compra_usd"]
                    self.precio_compra_soles = info["precio_compra_soles"]
                    self.precio_oferta_compra_usd = info["precio_oferta_compra_usd"]
                    self.precio_oferta_compra_soles = info["precio_oferta_compra_soles"]
                    self.garantia = info["garantia"]
                    self.marca = info["marca"]
                    self.categoria = info["categoria"]
                    self.detalle_promocion = info["detalle_promocion"]

                @property
                def precio_venta_soles(self):
                    return self.precio_compra_soles / Decimal('0.87') if self.precio_compra_soles else 0

                @property
                def precio_venta_oferta_soles(self):
                    return self.precio_oferta_compra_soles / Decimal('0.87') if self.precio_oferta_compra_soles else 0

                @property
                def margen_bruto_normal(self):
                    return self.precio_venta_soles - self.precio_compra_soles if self.precio_venta_soles > 0 else 0

                @property
                def igv_a_pagar_normal(self):
                    igv_cobrado = (self.precio_venta_soles * Decimal('0.18')) / Decimal('1.18')
                    igv_pagado = (self.precio_compra_soles * Decimal('0.18')) / Decimal('1.18')
                    return (igv_cobrado - igv_pagado) if (igv_cobrado - igv_pagado) > 0 else 0

                @property
                def impuesto_renta_normal(self):
                    return self.precio_venta_soles * Decimal('0.01') if self.precio_venta_soles > 0 else 0

                @property
                def costo_tarjeta_credito_normal(self):
                    return self.precio_venta_soles * Decimal('0.05') if self.precio_venta_soles > 0 else 0

                @property
                def utilidad_por_unidad_normal(self):
                    gastos_operativos = self.igv_a_pagar_normal + self.impuesto_renta_normal + self.costo_tarjeta_credito_normal
                    return self.margen_bruto_normal - gastos_operativos if self.margen_bruto_normal > 0 else 0

                @property
                def margen_bruto_oferta(self):
                    return self.precio_venta_oferta_soles - self.precio_oferta_compra_soles if self.precio_venta_oferta_soles > 0 else 0

                @property
                def igv_a_pagar_oferta(self):
                    if self.precio_venta_oferta_soles == 0:
                        return 0
                    igv_cobrado = (self.precio_venta_oferta_soles * Decimal('0.18')) / Decimal('1.18')
                    igv_pagado = (self.precio_oferta_compra_soles * Decimal('0.18')) / Decimal('1.18')
                    return (igv_cobrado - igv_pagado) if (igv_cobrado - igv_pagado) > 0 else 0

                @property
                def impuesto_renta_oferta(self):
                    return self.precio_venta_oferta_soles * Decimal('0.01') if self.precio_venta_oferta_soles > 0 else 0

                @property
                def costo_tarjeta_credito_oferta(self):
                    return self.precio_venta_oferta_soles * Decimal('0.05') if self.precio_venta_oferta_soles > 0 else 0

                @property
                def utilidad_por_unidad_oferta(self):
                    if self.precio_venta_oferta_soles == 0:
                        return 0
                    gastos_operativos = self.igv_a_pagar_oferta + self.impuesto_renta_oferta + self.costo_tarjeta_credito_oferta
                    return self.margen_bruto_oferta - gastos_operativos if self.margen_bruto_oferta > 0 else 0

            producto_unificado = ProductoUnificado(info)
            item = {
                "producto": producto_unificado,
                "precio_venta_publico": producto_unificado.precio_venta_soles,
                "precio_venta_oferta_publico": producto_unificado.precio_venta_oferta_soles,
                "almacen": {"nombre": "; ".join([f"{almacen}: {stock}" for almacen, stock in info["stock_por_almacen"].items()])},
                "precio_soles": producto_unificado.precio_compra_soles,
                "precio_oferta_soles": producto_unificado.precio_oferta_compra_soles,
                "margen_bruto_normal": producto_unificado.margen_bruto_normal,
                "igv_por_pagar_normal": producto_unificado.igv_a_pagar_normal,
                "impuesto_renta_normal": producto_unificado.impuesto_renta_normal,
                "costo_tarjeta_credito_normal": producto_unificado.costo_tarjeta_credito_normal,
                "utilidad_por_unidad_normal": producto_unificado.utilidad_por_unidad_normal,
                "margen_bruto_oferta": producto_unificado.margen_bruto_oferta,
                "igv_por_pagar_oferta": producto_unificado.igv_a_pagar_oferta,
                "impuesto_renta_oferta": producto_unificado.impuesto_renta_oferta,
                "costo_tarjeta_credito_oferta": producto_unificado.costo_tarjeta_credito_oferta,
                "utilidad_por_unidad_oferta": producto_unificado.utilidad_por_unidad_oferta,
            }
            productos_con_detalles.append(item)
            utilidad_bruta_total += item["margen_bruto_normal"] * Decimal(str(info["stock"]))
            utilidad_neta_total += item["utilidad_por_unidad_normal"] * Decimal(str(info["stock"]))

    return render_template(
        'productos.html',
        productos=productos_con_detalles,
        tipo_cambio=tipo_cambio,
        igv=igv,
        almacenes={almacen.id: almacen.nombre for almacen in Almacen.query.all()},
        utilidad_bruta_total=utilidad_bruta_total,
        utilidad_neta_total=utilidad_neta_total
    )

@routes.route('/recalcular-precios', methods=['GET'])
def recalcular_precios():
    try:
        recalcular_precios_en_soles(db.session)
        flash('Precios recalculados correctamente', 'success')
        return redirect(url_for('routes.get_productos'))
    except Exception as e:
        flash(f'Error al recalcular precios: {str(e)}', 'error')
        return redirect(url_for('routes.get_productos'))

@routes.route('/upload', methods=['GET', 'POST'])
def upload_file():
    almacenes = Almacen.query.all()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('routes.upload_file'))
        file = request.files['file']
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo', 'error')
            return redirect(url_for('routes.upload_file'))
        if file and file.filename.endswith('.csv'):
            try:
                file_path = os.path.join('uploads', file.filename)
                os.makedirs('uploads', exist_ok=True)
                file.save(file_path)
                flash('Archivo subido correctamente', 'success')
                return redirect(url_for('routes.vista_previa', archivo=file.filename))
            except Exception as e:
                flash(f'Error al subir el archivo: {str(e)}', 'error')
                return redirect(url_for('routes.upload_file'))
        else:
            flash('El archivo debe ser un CSV', 'error')
            return redirect(url_for('routes.upload_file'))
    return render_template('index.html', almacenes={almacen.id: almacen.nombre for almacen in almacenes})

@routes.route('/archivos')
def archivos():
    archivos = [f for f in os.listdir('uploads') if f.endswith('.csv')]
    archivos_procesados = {a.nombre: a.procesado for a in ArchivoProcesado.query.all()}
    almacenes = {almacen.id: almacen.nombre for almacen in Almacen.query.all()}
    return render_template('archivos.html', archivos=archivos, archivos_procesados=archivos_procesados, almacenes=almacenes)

@routes.route('/vista_previa/<archivo>')
def vista_previa(archivo):
    file_path = os.path.join('uploads', archivo)
    if os.path.exists(file_path):
        try:
            df = procesar_csv(file_path)
            columnas = df.columns.tolist()
            datos = df.to_dict(orient='records')
            for i, row in enumerate(datos):
                datos[i]['row_class'] = 'even' if i % 2 == 0 else 'odd'
            return render_template('vista_previa.html', archivo=archivo, columnas=columnas, datos=datos)
        except Exception as e:
            flash(f'Error al procesar la vista previa: {str(e)}', 'error')
            return redirect(url_for('routes.archivos'))
    else:
        flash('Archivo no encontrado', 'error')
        return redirect(url_for('routes.archivos'))

@routes.route('/procesar', methods=['POST'])
def procesar():
    archivo = request.form.get('archivo')
    almacen_id = request.form.get('almacen_id')
    file_path = os.path.join('uploads', archivo)
    if os.path.exists(file_path):
        try:
            cargar_csv_a_bd(file_path, almacen_id, db.session)
            archivo_db = ArchivoProcesado.query.filter_by(nombre=archivo).first()
            if not archivo_db:
                archivo_db = ArchivoProcesado(nombre=archivo, procesado=True)
                db.session.add(archivo_db)
            else:
                archivo_db.procesado = True
            db.session.commit()
            flash('Archivo procesado correctamente', 'success')
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}', 'error')
    else:
        flash('Archivo no encontrado', 'error')
    return redirect(url_for('routes.archivos'))

@routes.route('/borrar/<archivo>', methods=['POST'])
def borrar(archivo):
    file_path = os.path.join('uploads', archivo)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            archivo_db = ArchivoProcesado.query.filter_by(nombre=archivo).first()
            if archivo_db:
                db.session.delete(archivo_db)
                db.session.commit()
            flash('Archivo borrado correctamente', 'success')
        except Exception as e:
            flash(f'Error al borrar el archivo: {str(e)}', 'error')
    else:
        flash('Archivo no encontrado', 'error')
    return redirect(url_for('routes.archivos'))

@routes.route('/api/productos', methods=['GET'])
def api_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'codigo': p.codigo,
        'descripcion': p.descripcion,
        'stock': p.stock,
        'precio_compra_usd': float(p.precio_compra_usd),
        'precio_compra_soles': float(p.precio_compra_soles),
        'precio_oferta_compra_usd': float(p.precio_oferta_compra_usd) if p.precio_oferta_compra_usd else None,
        'precio_oferta_compra_soles': float(p.precio_oferta_compra_soles) if p.precio_oferta_compra_soles else None,
        'garantia': p.garantia,
        'marca': p.marca,
        'categoria': p.categoria,
        'detalle_promocion': p.detalle_promocion,
        'almacen_id': p.almacen_id
    } for p in productos])

@routes.route('/verify_categories')
def verify_categories():
    """
    Consulta todos los productos en la base de datos y muestra sus categorías originales,
    categorías generales y subcategorías.
    """
    try:
        # Consulta todos los productos con sus categorías
        productos = db.session.query(Producto).all()
        
        # Si no hay productos, renderiza la plantilla con una lista vacía
        if not productos:
            return render_template('verify_categories.html', productos=[])
        
        # Pasa la lista de productos directamente a la plantilla
        return render_template('verify_categories.html', productos=productos)
    
    except Exception as e:
        return f"Error al consultar las categorías: {str(e)}", 500
# Función para inicializar las rutas
def init_routes(app):
    app.register_blueprint(routes)