import os
import shutil
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def eliminar_archivos(carpeta):
    print(f"Eliminando archivos en la carpeta: {carpeta}")
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe, creando...")
        os.makedirs(carpeta)
    for filename in os.listdir(carpeta):
        file_path = os.path.join(carpeta, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"No se pudo eliminar el archivo {file_path}. Motivo: {e}")

def iniciar_sesion():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--remote-debugging-port={random.randint(49152, 65535)}")
    options.add_argument("--window-size=1920,1080")
    options.headless = False
    carpeta_descargas = os.path.abspath("descargas")
    prefs = {"download.default_directory": carpeta_descargas}
    options.add_experimental_option("prefs", prefs)
    
    eliminar_archivos(carpeta_descargas)
    eliminar_archivos(os.path.abspath("productos_deltron"))
    
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get('https://www.deltron.com.pe/login.php?prev=/index_2.php')
        # Esperar a que la página de login cargue completamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        return driver
    except Exception as e:
        print(f"Error al iniciar el driver: {e}")
        raise

def extraer_datos(url_almacenes, almacenes_seleccionados, driver, carpeta_descargas, progress_queue=None):
    print(f"Extrayendo datos a la carpeta: {carpeta_descargas}")
    
    carpeta_base = os.path.abspath("productos_deltron")
    os.makedirs(carpeta_base, exist_ok=True)
    total_almacenes = len(almacenes_seleccionados)
    processed_almacenes = 0
    
    for name, label in almacenes_seleccionados.items():
        try:
            driver.get(url_almacenes)
            print(f"URL actual: {driver.current_url}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
            )
            
            checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            print("Checkboxes encontrados en la página:")
            for cb in checkboxes:
                cb_name = cb.get_attribute("name")
                if cb_name:
                    print(f" - Checkbox con name='{cb_name}'")
            
            print(f"Buscando checkbox para '{label}' con name='{name}'")
            checkbox = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, name))
            )
            checkbox.click()
            print(f"Checkbox '{name}' clickeado exitosamente")
            
            boton_csv = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value=' CSV ']"))
            )
            boton_csv.click()
            print("Botón CSV clickeado, esperando descarga...")
            
            timeout = 60
            start_time = time.time()
            while time.time() - start_time < timeout:
                archivos_descargados = [f for f in os.listdir(carpeta_descargas) if f.endswith('.csv')]
                if archivos_descargados:
                    break
                time.sleep(1)
            if not archivos_descargados:
                print(f"Error: No se descargó ningún CSV para '{label}' después de {timeout} segundos")
                continue
            
            fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            carpeta_almacen = os.path.join(carpeta_base, f"{label}_{fecha_actual}")
            os.makedirs(carpeta_almacen, exist_ok=True)
            for archivo in archivos_descargados:
                archivo_origen = os.path.join(carpeta_descargas, archivo)
                archivo_destino = os.path.join(carpeta_almacen, f"{label}_{fecha_actual}_{archivo}")
                os.rename(archivo_origen, archivo_destino)
                print(f"Archivo '{archivo_origen}' movido a '{archivo_destino}'")
            
            driver.get(url_almacenes)
            checkbox = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, name))
            )
            checkbox.click()
            print(f"Checkbox '{name}' desmarcado")
            
            processed_almacenes += 1
            if progress_queue:
                progress = (processed_almacenes / total_almacenes) * 50
                progress_queue.put(progress)
        
        except Exception as e:
            print(f"Error al procesar el almacén '{label}': {str(e)}")
    
    # No cerrar el driver aquí, dejar que gui.py lo maneje
    print("Extracción completada, dejando el driver abierto para el siguiente paso.")

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
    "alm080": "Tacna",
    "alm005": "Lima - Otros Almacenes",
}