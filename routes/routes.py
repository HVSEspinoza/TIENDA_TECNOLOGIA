from flask import render_template, request, redirect, url_for, flash, jsonify
from decimal import Decimal
from models.models import Almacen, Producto, db, ArchivoProcesado
from utils.helpers import obtener_tipo_cambio, recalcular_precios_en_soles, cargar_csv_a_bd, procesar_csv
import os
import pandas as pd

def init_routes(app):
    @app.route('/')
    def index():
        almacenes = Almacen.query.all()
        return render_template('index.html', almacenes={almacen.id: almacen.nombre for almacen in almacenes})

    @app.route('/productos', methods=['GET', 'POST'])
    def get_productos():
        tipo_cambio = obtener_tipo_cambio()
        igv = Decimal('0.18')

        if request.method == 'POST':
            almacen_id = request.form.get('almacen_id')
            if almacen_id == '':
                productos = Producto.query.all()
            else:
                productos = Producto.query.filter_by(almacen_id=almacen_id).all()
        else:
            productos = Producto.query.all()

        productos_con_detalles = []
        utilidad_bruta_total = Decimal('0')
        utilidad_neta_total = Decimal('0')

        for producto in productos:
            precio_venta = producto.precio_venta_soles if producto.precio_venta_oferta_soles == 0 else producto.precio_venta_oferta_soles
            margen_bruto_unidad = producto.margen_bruto_normal if producto.precio_venta_oferta_soles == 0 else producto.margen_bruto_oferta
            utilidad_bruta_total += margen_bruto_unidad * Decimal(str(producto.stock))

            utilidad_neta_unidad = producto.utilidad_por_unidad_normal if producto.precio_venta_oferta_soles == 0 else producto.utilidad_por_unidad_oferta
            utilidad_neta_total += utilidad_neta_unidad * Decimal(str(producto.stock))

            almacen = Almacen.query.get(producto.almacen_id)
            productos_con_detalles.append({
                'producto': producto,
                'precio_venta_publico': producto.precio_venta_soles,
                'precio_venta_oferta_publico': producto.precio_venta_oferta_soles,
                'almacen': almacen,
                'precio_soles': producto.precio_compra_soles,
                'precio_oferta_soles': producto.precio_oferta_compra_soles,
                'margen_bruto_normal': producto.margen_bruto_normal,
                'igv_por_pagar_normal': producto.igv_a_pagar_normal,
                'impuesto_renta_normal': producto.impuesto_renta_normal,
                'costo_tarjeta_credito_normal': producto.costo_tarjeta_credito_normal,
                'utilidad_por_unidad_normal': producto.utilidad_por_unidad_normal,
                'margen_bruto_oferta': producto.margen_bruto_oferta,
                'igv_por_pagar_oferta': producto.igv_a_pagar_oferta,
                'impuesto_renta_oferta': producto.impuesto_renta_oferta,
                'costo_tarjeta_credito_oferta': producto.costo_tarjeta_credito_oferta,
                'utilidad_por_unidad_oferta': producto.utilidad_por_unidad_oferta,
            })

        return render_template(
            'productos.html',
            productos=productos_con_detalles,
            tipo_cambio=tipo_cambio,
            igv=igv,
            almacenes={almacen.id: almacen.nombre for almacen in Almacen.query.all()},
            utilidad_bruta_total=utilidad_bruta_total,
            utilidad_neta_total=utilidad_neta_total
        )

    @app.route('/recalcular-precios', methods=['GET'])
    def recalcular_precios():
        try:
            recalcular_precios_en_soles(db.session)
            flash('Precios recalculados correctamente', 'success')
            return redirect(url_for('get_productos'))
        except Exception as e:
            flash(f'Error al recalcular precios: {str(e)}', 'error')
            return redirect(url_for('get_productos'))

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        almacenes = Almacen.query.all()
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No se ha seleccionado ningún archivo', 'error')
                return redirect(url_for('upload_file'))
            file = request.files['file']
            if file.filename == '':
                flash('No se ha seleccionado ningún archivo', 'error')
                return redirect(url_for('upload_file'))
            if file and file.filename.endswith('.csv'):
                try:
                    file_path = os.path.join('uploads', file.filename)
                    os.makedirs('uploads', exist_ok=True)
                    file.save(file_path)
                    flash('Archivo subido correctamente', 'success')
                    return redirect(url_for('vista_previa', archivo=file.filename))
                except Exception as e:
                    flash(f'Error al subir el archivo: {str(e)}', 'error')
                    return redirect(url_for('upload_file'))
            else:
                flash('El archivo debe ser un CSV', 'error')
                return redirect(url_for('upload_file'))
        return render_template('index.html', almacenes={almacen.id: almacen.nombre for almacen in almacenes})

    @app.route('/archivos')
    def archivos():
        archivos = [f for f in os.listdir('uploads') if f.endswith('.csv')]
        archivos_procesados = {a.nombre: a.procesado for a in ArchivoProcesado.query.all()}
        almacenes = {almacen.id: almacen.nombre for almacen in Almacen.query.all()}
        return render_template('archivos.html', archivos=archivos, archivos_procesados=archivos_procesados, almacenes=almacenes)

    @app.route('/vista_previa/<archivo>')
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
                return redirect(url_for('archivos'))
        else:
            flash('Archivo no encontrado', 'error')
            return redirect(url_for('archivos'))

    @app.route('/procesar', methods=['POST'])
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
        return redirect(url_for('archivos'))

    @app.route('/borrar/<archivo>', methods=['POST'])
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
        return redirect(url_for('archivos'))