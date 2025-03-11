import pandas as pd
import unicodedata
from models.models import Producto

def obtener_tipo_cambio():
    return 3.85

def calcular_precio_con_igv(precio_dolares, tipo_cambio, igv):
    precio_soles = precio_dolares * tipo_cambio
    precio_soles_con_igv = precio_soles * (1 + igv)
    return precio_soles_con_igv

def procesar_csv(file_path):
    custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
    required_columns = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA"]
    
    custom_header_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                for col in custom_header]
    required_columns_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                   for col in required_columns]
    
    df = pd.read_csv(file_path, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
    normalized_columns = [unicodedata.normalize('NFKD', col.strip()).encode('ASCII', 'ignore').decode('ASCII').upper()
                         for col in df.columns]
    df.columns = normalized_columns
    
    available_columns = [col for col in custom_header_normalized if col in df.columns]
    missing_required = [col for col in required_columns_normalized if col not in df.columns]
    if missing_required:
        raise ValueError(f"El CSV no contiene todas las columnas requeridas. Faltan: {missing_required}, Encontradas: {df.columns.tolist()}")
    
    df = df[available_columns]
    
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
    
    df['STOCK'] = df['STOCK'].apply(convertir_stock)
    df['PRECIO DOLARES'] = df['PRECIO DOLARES'].apply(convertir_precio)
    if 'PROMOCION' in df.columns:
        df['PROMOCION'] = df['PROMOCION'].apply(convertir_precio)
    df['CODIGO'] = df['CODIGO'].apply(convertir_texto)
    df['DESCRIPCION'] = df['DESCRIPCION'].apply(lambda x: convertir_texto(x, 255))
    df['GARANTIA'] = df['GARANTIA'].apply(convertir_texto)
    df['MARCA'] = df['MARCA'].apply(lambda x: convertir_texto(x, 255))
    df['CATEGORIA'] = df['CATEGORIA'].apply(lambda x: convertir_texto(x, 255))
    if 'DETALLE PROMOCION' in df.columns:
        df['DETALLE PROMOCION'] = df['DETALLE PROMOCION'].apply(lambda x: convertir_texto(x, 255))
    
    return df

def cargar_csv_a_bd(csv_file, almacen_id, db_session):
    try:
        data = procesar_csv(csv_file)
        tipo_cambio = obtener_tipo_cambio()
        igv = 0.18
        db_session.query(Producto).filter_by(almacen_id=almacen_id).delete()
        for _, row in data.iterrows():
            precio_soles_con_igv = calcular_precio_con_igv(row['PRECIO DOLARES'], tipo_cambio, igv)
            promocion_valor = row['PROMOCION'] if 'PROMOCION' in row else None
            detalle_promocion = row['DETALLE PROMOCION'] if 'DETALLE PROMOCION' in row else ''
            nuevo_producto = Producto(
                codigo=row['CODIGO'], descripcion=row['DESCRIPCION'], stock=row['STOCK'],
                precio_dolares=row['PRECIO DOLARES'], precio_soles=precio_soles_con_igv,
                garantia=row['GARANTIA'], marca=row['MARCA'], categoria=row['CATEGORIA'],
                promocion=promocion_valor, detalle_promocion=detalle_promocion, almacen_id=almacen_id
            )
            db_session.add(nuevo_producto)
        db_session.commit()
        print(f"Datos del archivo {csv_file} cargados correctamente.")
    except Exception as e:
        print(f"Error al procesar {csv_file}: {e}")
        db_session.rollback()
        raise