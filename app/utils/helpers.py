import pandas as pd
import unicodedata
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
from sqlalchemy.orm import Session
from app.models import Producto, Almacen
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
    
    df = pd.read_csv(file_path, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
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
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

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
            if 'driver' in locals():
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

        # Mapeo de categorías actuales a jerarquía optimizada
        categoria_map = {
            # Accesorios
            "acc, muebles de computo": {"categoria_general": "Accesorios", "subcategoria": "Muebles de Computación"},
            "accesorios": {"categoria_general": "Accesorios", "subcategoria": "Generales"},
            "accesorios ensamblaje": {"categoria_general": "Accesorios", "subcategoria": "Ensamblaje"},
            "accesorios usb": {"categoria_general": "Accesorios", "subcategoria": "USB"},
            "aire acond precision, acc": {"categoria_general": "Accesorios", "subcategoria": "Aire Acondicionado de Precisión"},
            "asterisk, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Asterisk"},
            "audio, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Audio"},
            "cases, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Carcasas"},
            "gaming, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Gaming"},
            "monitores, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Monitores"},
            "mouse pad/mat, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Mouse Pads"},
            "notebook, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Notebooks"},
            "tablet, accesorios de": {"categoria_general": "Accesorios", "subcategoria": "Tablets"},
            "t celulares, accesorios": {"categoria_general": "Accesorios", "subcategoria": "Teléfonos Celulares"},

            # Audio
            "audio, auricular c/mic": {"categoria_general": "Audio", "subcategoria": "Auriculares con Micrófono"},
            "audio, auricular c/mic gm": {"categoria_general": "Audio", "subcategoria": "Auriculares Gaming con Micrófono"},
            "audio, parlante inalamb": {"categoria_general": "Audio", "subcategoria": "Parlantes Inalámbricos"},
            "audio, parlante usb": {"categoria_general": "Audio", "subcategoria": "Parlantes USB"},

            # Barebones y Computadoras
            "barebones para aio": {"categoria_general": "Computadoras", "subcategoria": "Barebones All-in-One"},
            "barebones para pc": {"categoria_general": "Computadoras", "subcategoria": "Barebones PC"},
            "chromebook": {"categoria_general": "Computadoras", "subcategoria": "Chromebooks"},
            "computadora aio celeron": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Celeron"},
            "computadora aio core i3": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Core i3"},
            "computadora aio core i5": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Core i5"},
            "computadora aio core i7": {"categoria_general": "Computadoras", "subcategoria": "All-in-One Core i7"},
            "computadora core i5": {"categoria_general": "Computadoras", "subcategoria": "PC Core i5"},
            "computadora core i7": {"categoria_general": "Computadoras", "subcategoria": "PC Core i7"},
            "computadora gaming": {"categoria_general": "Computadoras", "subcategoria": "Gaming"},
            "computadora workstation": {"categoria_general": "Computadoras", "subcategoria": "Workstations"},

            # Cámaras y Smart Home
            "camara, webcam": {"categoria_general": "Cámaras", "subcategoria": "Webcams"},
            "smart home - camaras": {"categoria_general": "Smart Home", "subcategoria": "Cámaras"},
            "smart home - enchufes": {"categoria_general": "Smart Home", "subcategoria": "Enchufes"},
            "smart home - luces": {"categoria_general": "Smart Home", "subcategoria": "Luces"},

            # Carcasas y Fuentes
            "cases micro atx": {"categoria_general": "Carcasas", "subcategoria": "Micro ATX"},
            "cases sin fuente p/gamers": {"categoria_general": "Carcasas", "subcategoria": "Sin Fuente para Gamers"},
            "cases, fan": {"categoria_general": "Carcasas", "subcategoria": "Ventiladores"},
            "cases, fuente para": {"categoria_general": "Fuentes", "subcategoria": "ATX Estándar"},
            "cases, fuente para gaming": {"categoria_general": "Fuentes", "subcategoria": "Gaming"},
            "fuente atx": {"categoria_general": "Fuentes", "subcategoria": "ATX"},
            "fuente sfx": {"categoria_general": "Fuentes", "subcategoria": "SFX"},

            # Consolas
            "consolas ps5": {"categoria_general": "Consolas", "subcategoria": "PlayStation 5"},
            "consolas, otras marcas": {"categoria_general": "Consolas", "subcategoria": "Otras Marcas"},

            # Coolers
            "cooler liquido cpu 120": {"categoria_general": "Coolers", "subcategoria": "Líquidos 120mm"},
            "cooler liquido cpu 240": {"categoria_general": "Coolers", "subcategoria": "Líquidos 240mm"},

            # CPUs
            "cpu amd athlon sam4": {"categoria_general": "Procesadores", "subcategoria": "AMD Athlon AM4"},
            "cpu amd ryzen 3 sam4 3xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 3 3xxx AM4"},
            "cpu amd ryzen 3 sam5 8xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 3 8xxx AM5"},
            "cpu amd ryzen 5 sam4 3xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 3xxx AM4"},
            "cpu amd ryzen 5 sam4 4xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 4xxx AM4"},
            "cpu amd ryzen 5 sam4 5xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 5xxx AM4"},
            "cpu amd ryzen 5 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 7xxx AM5"},
            "cpu amd ryzen 5 sam5 8xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 8xxx AM5"},
            "cpu amd ryzen 5 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 5 9xxx AM5"},
            "cpu amd ryzen 7 sam4 5xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 7 5xxx AM4"},
            "cpu amd ryzen 7 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 7 7xxx AM5"},
            "cpu amd ryzen 7 sam5 8xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 7 8xxx AM5"},
            "cpu amd ryzen 7 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 7 9xxx AM5"},
            "cpu amd ryzen 9 sam5 7xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 9 7xxx AM5"},
            "cpu amd ryzen 9 sam5 9xxx": {"categoria_general": "Procesadores", "subcategoria": "AMD Ryzen 9 9xxx AM5"},

            # Discos y SSDs
            "disco duro 2.5 sata": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros 2.5 SATA"},
            "disco duro 3.5 sata": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros 3.5 SATA"},
            "disco duro externo": {"categoria_general": "Almacenamiento", "subcategoria": "Discos Duros Externos"},
            "ssd 2.5 sata": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs 2.5 SATA"},
            "ssd m.2 nvme": {"categoria_general": "Almacenamiento", "subcategoria": "SSDs M.2 NVMe"},

            # Impresoras
            "aire acond. de precision": {"categoria_general": "Climatización", "subcategoria": "Aire Acondicionado de Precisión"},
            "comercial laser": {"categoria_general": "Impresoras", "subcategoria": "Láser"},
            "comercial laser multi": {"categoria_general": "Impresoras", "subcategoria": "Multifuncional Láser"},
            "comercial matricial": {"categoria_general": "Impresoras", "subcategoria": "Matricial"},
            "comercial tanque tinta": {"categoria_general": "Impresoras", "subcategoria": "Tanque de Tinta"},
            "comercial tanque tinta mu": {"categoria_general": "Impresoras", "subcategoria": "Multifuncional Tanque de Tinta"},
            "comercial ticketera": {"categoria_general": "Impresoras", "subcategoria": "Ticketera"},
            "consumo tanque tinta": {"categoria_general": "Impresoras", "subcategoria": "Tanque de Tinta Consumo"},
            "consumo tanque tinta mult": {"categoria_general": "Impresoras", "subcategoria": "Multifuncional Tanque de Tinta Consumo"},
            "suminist p/impr, botellas": {"categoria_general": "Suministros", "subcategoria": "Botellas de Tinta"},
            "suminist p/impres, cintas": {"categoria_general": "Suministros", "subcategoria": "Cintas de Impresión"},

            # Memorias y Componentes
            "componentes, repuestos": {"categoria_general": "Componentes", "subcategoria": "Repuestos"},
            "lectoras de tarjetas": {"categoria_general": "Componentes", "subcategoria": "Lectoras de Tarjetas"},
            "memoria ddr4": {"categoria_general": "Memorias", "subcategoria": "DDR4"},
            "memoria ddr5": {"categoria_general": "Memorias", "subcategoria": "DDR5"},
            "memoria ddr5 ecc": {"categoria_general": "Memorias", "subcategoria": "DDR5 ECC"},
            "memoria ram ddr3": {"categoria_general": "Memorias", "subcategoria": "DDR3"},

            # Monitores
            "monitor curvo 27": {"categoria_general": "Monitores", "subcategoria": "Curvos 27"},
            "monitor curvo 32": {"categoria_general": "Monitores", "subcategoria": "Curvos 32"},
            "monitor gaming curvo 27": {"categoria_general": "Monitores", "subcategoria": "Gaming Curvos 27"},
            "monitor gaming curvo 34": {"categoria_general": "Monitores", "subcategoria": "Gaming Curvos 34"},
            "monitor gaming plano 24": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 24"},
            "monitor gaming plano 25": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 25"},
            "monitor gaming plano 27": {"categoria_general": "Monitores", "subcategoria": "Gaming Planos 27"},
            "monitor plano 21.45": {"categoria_general": "Monitores", "subcategoria": "Planos 21-22"},
            "monitor plano 23": {"categoria_general": "Monitores", "subcategoria": "Planos 23"},
            "monitor plano 27": {"categoria_general": "Monitores", "subcategoria": "Planos 27"},
            "monitor plano 31.5": {"categoria_general": "Monitores", "subcategoria": "Planos 31-32"},

            # Mouse y Teclados
            "mouse inalambrico": {"categoria_general": "Periféricos", "subcategoria": "Mouse Inalámbricos"},
            "mouse para gamers": {"categoria_general": "Periféricos", "subcategoria": "Mouse Gaming"},
            "mouse usb": {"categoria_general": "Periféricos", "subcategoria": "Mouse USB"},
            "teclado inalambrico": {"categoria_general": "Periféricos", "subcategoria": "Teclados Inalámbricos"},
            "teclado para gamers": {"categoria_general": "Periféricos", "subcategoria": "Teclados Gaming"},
            "teclado usb": {"categoria_general": "Periféricos", "subcategoria": "Teclados USB"},
            "teclado+mouse combo kit": {"categoria_general": "Periféricos", "subcategoria": "Kits Teclado + Mouse"},
            "teclado+mouse kit inalamb": {"categoria_general": "Periféricos", "subcategoria": "Kits Inalámbricos"},

            # Notebooks
            "notebook 2-in-1 celeron": {"categoria_general": "Notebooks", "subcategoria": "2-in-1 Celeron"},
            "notebook amd athlon": {"categoria_general": "Notebooks", "subcategoria": "AMD Athlon"},
            "notebook amd ryzen 3": {"categoria_general": "Notebooks", "subcategoria": "AMD Ryzen 3"},
            "notebook amd ryzen 5": {"categoria_general": "Notebooks", "subcategoria": "AMD Ryzen 5"},
            "notebook amd ryzen 7": {"categoria_general": "Notebooks", "subcategoria": "AMD Ryzen 7"},
            "notebook celeron": {"categoria_general": "Notebooks", "subcategoria": "Celeron"},
            "notebook core i3": {"categoria_general": "Notebooks", "subcategoria": "Core i3"},
            "notebook core i5": {"categoria_general": "Notebooks", "subcategoria": "Core i5"},
            "notebook core i7": {"categoria_general": "Notebooks", "subcategoria": "Core i7"},
            "notebook core ultra 5": {"categoria_general": "Notebooks", "subcategoria": "Core Ultra 5"},
            "notebook gaming core i5": {"categoria_general": "Notebooks", "subcategoria": "Gaming Core i5"},
            "notebook gaming core i7": {"categoria_general": "Notebooks", "subcategoria": "Gaming Core i7"},
            "notebook gaming ryzen 5": {"categoria_general": "Notebooks", "subcategoria": "Gaming Ryzen 5"},
            "notebook gaming ryzen 7": {"categoria_general": "Notebooks", "subcategoria": "Gaming Ryzen 7"},
            "notebook, maletin/mochila": {"categoria_general": "Accesorios", "subcategoria": "Maletines y Mochilas"},

            # Otros
            "productos sin clasificar": {"categoria_general": "Otros", "subcategoria": "Sin Clasificar"},
            "rep tb - otros hw": {"categoria_general": "Otros", "subcategoria": "Hardware Variado"},
            "servicios otros": {"categoria_general": "Otros", "subcategoria": "Servicios"},

            # Redes
            "red, switch basico": {"categoria_general": "Redes", "subcategoria": "Switches Básicos"},

            # Sillas y Televisores
            "sillas gamer": {"categoria_general": "Mobiliario", "subcategoria": "Sillas Gaming"},
            "televisores led/smart tv": {"categoria_general": "Televisores", "subcategoria": "LED/Smart TV"},
            "televisores, racks para": {"categoria_general": "Accesorios", "subcategoria": "Racks para TV"},

            # Software
            "ms esd aplicaciones": {"categoria_general": "Software", "subcategoria": "Aplicaciones ESD"},
            "ms esd office": {"categoria_general": "Software", "subcategoria": "Office ESD"},
            "ms esd office 365": {"categoria_general": "Software", "subcategoria": "Office 365 ESD"},
            "ms esd windows business": {"categoria_general": "Software", "subcategoria": "Windows Business ESD"},
            "ms esd windows consumer": {"categoria_general": "Software", "subcategoria": "Windows Consumer ESD"},
            "ms windows consumer": {"categoria_general": "Software", "subcategoria": "Windows Consumer"},
            "ms windows server": {"categoria_general": "Software", "subcategoria": "Windows Server"},
            "software, antivirus": {"categoria_general": "Software", "subcategoria": "Antivirus"},

            # Tablets
            "tablet android": {"categoria_general": "Tablets", "subcategoria": "Android"},

            # UPS
            "ups interactivo": {"categoria_general": "UPS", "subcategoria": "Interactivo"},

            # Video
            "video, pci exp nvidia gam": {"categoria_general": "Tarjetas de Video", "subcategoria": "PCI Express NVIDIA Gaming"},
            "video, pci express nvidia": {"categoria_general": "Tarjetas de Video", "subcategoria": "PCI Express NVIDIA"},

            # Teléfonos Celulares
            "t celulares basicos": {"categoria_general": "Teléfonos Celulares", "subcategoria": "Básicos"},
            "t celulares, smartwatches": {"categoria_general": "Teléfonos Celulares", "subcategoria": "Smartwatches"},
        }

        categorias_no_mapeadas = set()  # Para rastrear categorías no mapeadas

        for _, row in data.iterrows():
            precio_soles_con_igv = calcular_precio_con_igv(row['PRECIO DOLARES'], tipo_cambio['venta'], igv)
            precio_oferta_usd = row['PROMOCION'] if 'PROMOCION' in row and pd.notna(row['PROMOCION']) else None
            precio_oferta_soles = calcular_precio_con_igv(precio_oferta_usd, tipo_cambio['venta'], igv) if precio_oferta_usd else None
            detalle_promocion = row['DETALLE PROMOCION'] if 'DETALLE PROMOCION' in row and pd.notna(row['DETALLE PROMOCION']) else ''

            # Obtener la categoría del CSV y mapearla a la nueva jerarquía
            categoria_csv = row['CATEGORIA'].lower().strip() if isinstance(row['CATEGORIA'], str) and pd.notna(row['CATEGORIA']) else ''
            mapped_categoria = categoria_map.get(categoria_csv, {
                "categoria_general": "Sin Clasificar",
                "subcategoria": "Sin Clasificar"
            })
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