from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def inspeccionar_pagina_sunat(max_intentos=3):
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
            
            # Buscar la tabla del calendario
            tabla_calendario = soup.find('table', {'class': 'calendar-table'})
            if not tabla_calendario:
                raise ValueError("No se encontró la tabla del calendario con class='calendar-table'")
            
            # Buscar todas las celdas de los días
            dias = tabla_calendario.find_all('td', class_='calendar-day')
            
            # Buscar el día actual (o el último día con datos)
            ultimo_dia_con_datos = None
            fecha_ultimo_dia = None
            
            for dia in dias:
                # Obtener la fecha del día
                fecha_dia = dia.get('data-date')  # Ejemplo: "2025-03-14T05:00:00.000Z"
                if not fecha_dia:
                    continue
                
                # Buscar los eventos (Compra y Venta)
                eventos = dia.find_all('div', class_='event')
                if len(eventos) == 2:  # Asegurarse de que tenga Compra y Venta
                    ultimo_dia_con_datos = dia
                    fecha_ultimo_dia = fecha_dia
            
            if not ultimo_dia_con_datos:
                raise ValueError("No se encontraron días con datos de tipo de cambio")
            
            # Extraer la fecha
            fecha = fecha_ultimo_dia.split('T')[0]  # "2025-03-14"
            
            # Extraer Compra y Venta
            eventos = ultimo_dia_con_datos.find_all('div', class_='event')
            compra = float(eventos[0].find('strong').next_sibling.strip())  # Ejemplo: 3.663
            venta = float(eventos[1].find('strong').next_sibling.strip())   # Ejemplo: 3.670
            
            print(f"\nÚltimo día con datos encontrado:")
            print(f"Fecha: {fecha}")
            print(f"Compra: {compra}")
            print(f"Venta: {venta}")
            
            return {'compra': compra, 'venta': venta, 'date': fecha}
        
        except Exception as e:
            print(f"Error en el intento {intento + 1}: {e}")
            if intento < max_intentos - 1:
                time.sleep(5)
            else:
                print("Se agotaron los intentos. Revisa la conexión o la configuración.")
                raise
        
        finally:
            if 'driver' in locals():
                driver.quit()

if __name__ == "__main__":
    inspeccionar_pagina_sunat()