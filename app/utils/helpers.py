import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
from sqlalchemy.orm import Session
from app.models import Producto, Almacen
from app.config.category_mappings import categoria_map, mapear_categoria_dinamica  # Importar ambas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from decimal import Decimal

def procesar_csv(file_path):
    """
    Procesa un archivo CSV, normaliza los encabezados y aplica conversiones a los datos.
    """
    custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
    required_columns = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA"]
    
    custom_header_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                for col in custom_header]
    required_columns_normalized = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').upper() 
                                   for col in required_columns]
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV {file_path}: {str(e)}")

    # Validar que el CSV tenga al menos las columnas requeridas
    if len(df.columns) < len(required_columns):
        raise ValueError(f"El CSV tiene menos columnas de las requeridas. Columnas esperadas: {required_columns}, Columnas encontradas: {df.columns.tolist()}")

    normalized_columns = [unicodedata.normalize('NFKD', col.strip()).encode('ASCII', 'ignore').decode('ASCII').upper()
                         for col in df.columns]
    print(f"Columnas encontradas en el CSV {file_path}: {normalized_columns}")
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
            print(f"Advertencia: Stock no válido '{valor}'. Se asumirá 0.")
            return 0
    
    def convertir_precio(valor):
        try:
            valor_str = str(valor).replace('$', '').strip()
            return float(valor_str) if valor_str != '' else 0.0
        except (ValueError, TypeError):
            print(f"Advertencia: Precio no válido '{valor}'. Se asumirá 0.0.")
            return 0.0
    
    def convertir_texto(valor, max_length=255):
        if pd.isna(valor) or str(valor).strip() == '':
            return 'sin_valor'
        texto = str(valor).strip()
        return texto[:max_length] if len(texto) > max_length else texto
    
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

def calcular_precio_con_igv(precio_usd, tipo_cambio, igv):
    """
    Calcula el precio en soles incluyendo IGV a partir del precio en dólares.
    """
    tipo_cambio = Decimal(str(tipo_cambio))
    precio_usd = Decimal(str(precio_usd)) if not isinstance(precio_usd, Decimal) else precio_usd
    precio_soles = precio_usd * tipo_cambio
    factor_igv = Decimal(str(1 + igv))
    precio_con_igv = precio_soles * factor_igv
    return Decimal(str(round(precio_con_igv, 2)))

def obtener_tipo_cambio(max_intentos=3):
    """
    Obtiene el tipo de cambio (USD a PEN) desde SUNAT usando Selenium y lo guarda en exchange_rates.json.
    """
    cache_file = "exchange_rates.json"
    hoy = datetime.now().date()
    
    # Intentar leer el tipo de cambio desde el caché
    try:
        if os.path.exists(cache_file):
            if os.path.getsize(cache_file) == 0:
                print(f"El archivo {cache_file} está vacío. Se procederá a obtener el tipo de cambio desde SUNAT.")
            else:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    if not data:
                        print(f"El archivo {cache_file} contiene un JSON vacío. Se procederá a obtener el tipo de cambio desde SUNAT.")
                    else:
                        fecha_guardada = datetime.strptime(data['date'], '%Y-%m-%d').date()
                        if fecha_guardada == hoy:
                            print(f"Usando tipo de cambio desde caché: {data}")
                            return data
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al leer el archivo de caché {cache_file}: {e}. Se procederá a obtener el tipo de cambio desde SUNAT.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo de caché {cache_file}: {e}")

    # Configurar Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = None
    for intento in range(max_intentos):
        try:
            print(f"Intento {intento + 1} de {max_intentos}")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            url = "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"
            driver.get(url)
            time.sleep(2)
            
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            tabla_calendario = soup.find('table', {'class': 'calendar-table'})
            if not tabla_calendario:
                raise ValueError("No se encontró la tabla del calendario con class='calendar-table'")
            
            dias = tabla_calendario.find_all('td', class_='calendar-day')
            ultimo_dia_con_datos = None
            fecha_ultimo_dia = None
            
            for dia in dias:
                fecha_dia = dia.get('data-date')
                if not fecha_dia:
                    continue
                try:
                    datetime.strptime(fecha_dia.split('T')[0], '%Y-%m-%d')  # Validar formato de fecha
                except ValueError:
                    continue
                eventos = dia.find_all('div', class_='event')
                if len(eventos) == 2:
                    ultimo_dia_con_datos = dia
                    fecha_ultimo_dia = fecha_dia
            
            if not ultimo_dia_con_datos:
                raise ValueError("No se encontraron días con datos de tipo de cambio")
            
            fecha = fecha_ultimo_dia.split('T')[0]
            eventos = ultimo_dia_con_datos.find_all('div', class_='event')
            compra = float(eventos[0].find('strong').next_sibling.strip())
            venta = float(eventos[1].find('strong').next_sibling.strip())
            
            tipo_cambio = {
                'compra': compra,
                'venta': venta,
                'date': fecha
            }
            
            try:
                with open(cache_file, 'w') as f:
                    json.dump(tipo_cambio, f)
                print(f"Tipo de cambio actualizado desde SUNAT y guardado en {cache_file}: {tipo_cambio}")
            except Exception as e:
                print(f"Error al guardar el tipo de cambio en {cache_file}: {e}")
            
            return tipo_cambio
        
        except Exception as e:
            print(f"Error en el intento {intento + 1}: {e}")
            if intento < max_intentos - 1:
                time.sleep(5)
            else:
                print("Se agotaron los intentos. Usando valores por defecto.")
                return {'compra': 3.663, 'venta': 3.670, 'date': '2025-03-14'}
        
        finally:
            if driver:
                driver.quit()

def cargar_csv_a_bd(csv_file, almacen_id, db_session):
    """
    Carga los datos de un CSV a la base de datos.
    """
    try:
        data = procesar_csv(csv_file)
        tipo_cambio = obtener_tipo_cambio()
        igv = 0.18
        db_session.query(Producto).filter_by(almacen_id=almacen_id).delete()

        categorias_no_mapeadas = set()  # Para rastrear categorías no mapeadas
        for _, row in data.iterrows():
            precio_soles_con_igv = calcular_precio_con_igv(row['PRECIO DOLARES'], tipo_cambio['venta'], igv)
            precio_oferta_usd = row['PROMOCION'] if 'PROMOCION' in row and pd.notna(row['PROMOCION']) else None
            precio_oferta_soles = calcular_precio_con_igv(precio_oferta_usd, tipo_cambio['venta'], igv) if precio_oferta_usd else None
            detalle_promocion = row['DETALLE PROMOCION'] if 'DETALLE PROMOCION' in row and pd.notna(row['DETALLE PROMOCION']) else ''

            # Obtener la categoría del CSV y mapearla a la nueva jerarquía
            categoria_csv = row['CATEGORIA'].lower().strip() if isinstance(row['CATEGORIA'], str) and pd.notna(row['CATEGORIA']) else ''
            mapped_categoria = mapear_categoria_dinamica(categoria_csv)
            print(f"Procesando categoría: {categoria_csv} -> General: {mapped_categoria['categoria_general']}, Sub: {mapped_categoria['subcategoria']}")

            # Registrar categorías no mapeadas
            if mapped_categoria['categoria_general'] == "Sin Clasificar":
                categorias_no_mapeadas.add(categoria_csv)

            nuevo_producto = Producto(
                codigo=str(row['CODIGO']) if pd.notna(row['CODIGO']) else '',
                descripcion=str(row['DESCRIPCION']) if pd.notna(row['DESCRIPCION']) else '',
                stock=int(row['STOCK']) if pd.notna(row['STOCK']) else 0,
                precio_compra_usd=Decimal(str(row['PRECIO DOLARES'])) if pd.notna(row['PRECIO DOLARES']) else Decimal('0.00'),
                precio_compra_soles=precio_soles_con_igv,
                precio_oferta_compra_usd=Decimal(str(precio_oferta_usd)) if precio_oferta_usd is not None else None,
                precio_oferta_compra_soles=precio_oferta_soles,
                garantia=str(row['GARANTIA']) if pd.notna(row['GARANTIA']) else '',
                marca=str(row['MARCA']) if pd.notna(row['MARCA']) else '',
                categoria=str(row['CATEGORIA']) if pd.notna(row['CATEGORIA']) else '',
                categoria_general=mapped_categoria['categoria_general'],
                subcategoria=mapped_categoria['subcategoria'],
                detalle_promocion=detalle_promocion,
                almacen_id=almacen_id
            )
            db_session.add(nuevo_producto)

        # Mostrar categorías no mapeadas al final
        if categorias_no_mapeadas:
            print("Advertencia: Se encontraron categorías no mapeadas en el categoria_map:")
            for cat in categorias_no_mapeadas:
                print(f" - {cat}")

        db_session.commit()
        print(f"Datos del archivo {csv_file} cargados correctamente.")
    except Exception as e:
        print(f"Error al procesar {csv_file}: {e}")
        db_session.rollback()
        raise

def recalcular_precios_en_soles(db_session):
    """
    Recalcula los precios en soles para todos los productos en la base de datos usando el tipo de cambio actual.
    """
    try:
        tipo_cambio = obtener_tipo_cambio()
        igv = 0.18
        productos = db_session.query(Producto).all()

        for producto in productos:
            producto.precio_compra_soles = calcular_precio_con_igv(
                producto.precio_compra_usd, tipo_cambio['venta'], igv
            )
            if producto.precio_oferta_compra_usd:
                producto.precio_oferta_compra_soles = calcular_precio_con_igv(
                    producto.precio_oferta_compra_usd, tipo_cambio['venta'], igv
                )
            else:
                producto.precio_oferta_compra_soles = None

        db_session.commit()
        print("Precios en soles actualizados correctamente.")
    except Exception as e:
        print(f"Error al recalcular precios en soles: {e}")
        db_session.rollback()
        raise