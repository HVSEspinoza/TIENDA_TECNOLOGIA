import pandas as pd
import unicodedata
from models.models import Producto
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuración de Selenium
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Modo headless para no mostrar el navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Función para obtener la página con Selenium
def fetch_sunat_page():
    driver = setup_driver()
    try:
        url = "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"
        driver.get(url)
        
        # Esperar a que cargue el calendario
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-bordered"))
        )
        time.sleep(5)  # Espera adicional para asegurar el renderizado

        html_content = driver.page_source
        return html_content
    except Exception as e:
        print(f"Error al obtener la página de SUNAT con Selenium: {e}")
        return None
    finally:
        driver.quit()

# Función para extraer el tipo de cambio del día actual
def extract_current_exchange_rate():
    html_content = fetch_sunat_page()
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    today = datetime.now()
    # Formato sin ceros iniciales: _2025_3_12
    today_str = f"_{today.year}_{today.month}_{today.day}"

    # Buscar la celda <td> para el día actual
    current_cell = soup.find('td', class_=lambda x: x and today_str in x)

    if not current_cell:
        print(f"No se encontró la celda para {today_str}. Buscando la más reciente...")
        # Buscar todas las celdas con clase 'current' y tomar la más reciente
        cells = soup.find_all('td', class_=lambda x: x and 'current' in x)
        if cells:
            current_cell = max(cells, key=lambda x: x.get('data-date', '1970-01-01T00:00:00.000Z'))
        else:
            print("No se encontraron celdas con clase 'current' en el HTML.")
            return None

    if current_cell:
        # Extraer compra y venta
        compra_div = current_cell.find('div', class_=lambda x: x and 'normal-all-day' in x)
        venta_div = current_cell.find('div', class_=lambda x: x and 'pap-all-day' in x)

        if not compra_div or not venta_div:
            print("No se encontraron los valores de compra y venta.")
            return None

        # Extraer los valores numéricos
        compra_text = compra_div.text.replace('Compra', '').strip().replace(',', '.')
        venta_text = venta_div.text.replace('Venta', '').strip().replace(',', '.')

        try:
            compra = float(compra_text)
            venta = float(venta_text)
        except ValueError as e:
            print(f"Error al convertir los valores a números: {e}")
            return None

        return {
            "compra": compra,
            "venta": venta,
            "date": today.strftime("%Y-%m-%d")
        }
    return None

# Guardar en archivo JSON para caché
EXCHANGE_RATE_FILE = 'exchange_rates.json'

def save_exchange_rates(rates):
    with open(EXCHANGE_RATE_FILE, 'w') as f:
        json.dump(rates, f, indent=2)

# Cargar tasas de cambio desde caché
def load_exchange_rates():
    if os.path.exists(EXCHANGE_RATE_FILE):
        with open(EXCHANGE_RATE_FILE, 'r') as f:
            return json.load(f)
    return None

# Función principal para obtener el tipo de cambio
def obtener_tipo_cambio():
    # Primero intentar cargar desde caché
    cached_rate = load_exchange_rates()
    if cached_rate and datetime.strptime(cached_rate["date"], "%Y-%m-%d").date() == datetime.now().date():
        print("Usando tipo de cambio desde caché:", cached_rate)
        return cached_rate["venta"]  # Usamos la venta como referencia principal

    # Si no hay caché o la fecha no coincide, extraer desde SUNAT
    new_rate = extract_current_exchange_rate()
    if new_rate:
        save_exchange_rates(new_rate)
        print("Tipo de cambio actualizado desde SUNAT:", new_rate)
        return new_rate["venta"]
    else:
        print("No se pudo obtener el tipo de cambio desde SUNAT, usando valor por defecto: 3.85")
        return 3.85  # Valor por defecto si falla la extracción

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