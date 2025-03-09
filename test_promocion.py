import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_driver():
    """Inicia el navegador Chrome con las opciones necesarias."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.headless = False

    carpeta_descargas = os.path.abspath("descargas_test")
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas)
    prefs = {"download.default_directory": carpeta_descargas}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def buscar_promocion(driver, codigo):
    """Accede a la página del producto y extrae el precio promocional y detalles de promociones adicionales."""
    try:
        url_producto = f"https://www.deltron.com.pe/modulos/productos/items/producto.php?item_number={codigo}"
        print(f"Accediendo a la página del producto: {url_producto}")
        driver.get(url_producto)
        time.sleep(5)

        precios_secciones = driver.find_elements(By.CLASS_NAME, "product-price-discount")
        if not precios_secciones:
            print("No se encontraron elementos con clase 'product-price-discount'.")
            return None, []

        precio_promo_valor = None
        promociones_adicionales = []

        for seccion in precios_secciones:
            html_seccion = seccion.get_attribute('outerHTML')
            print(f"Sección: {html_seccion}")

            # Buscar precio promocional
            try:
                tipo_precio = seccion.find_element(By.CLASS_NAME, "product-price-type")
                if "Precio Promoción" in tipo_precio.text:
                    precio_promo_elem = seccion.find_element(By.CSS_SELECTOR, "b.aqui1")
                    precio_promo = precio_promo_elem.text.strip()
                    precio_promo_valor = float(precio_promo.replace("US $", "").replace("+ IGV", "").strip())
                    print(f"Promoción encontrada: {precio_promo} (Valor: {precio_promo_valor})")
            except:
                pass

            # Buscar promociones adicionales
            try:
                promo_elem = seccion.find_element(By.CSS_SELECTOR, "[data-promo]")
                promo_id = promo_elem.get_attribute("data-promo")
                promo_texto = promo_elem.find_element(By.TAG_NAME, "img").get_attribute("title").strip()
                if promo_id and promo_texto:
                    promociones_adicionales.append(f"{promo_id}: {promo_texto}")
            except:
                pass

        if precio_promo_valor is None:
            print("No se encontró 'Precio Promoción'.")
        if not promociones_adicionales:
            print("No se encontraron promociones adicionales.")
        else:
            print(f"Promociones adicionales encontradas: {promociones_adicionales}")

        return precio_promo_valor, promociones_adicionales

    except Exception as e:
        print(f"Error general al buscar promoción para {codigo}: {e}")
        return None, []

def probar_promocion(codigos):
    """Prueba la funcionalidad de búsqueda de promociones para una lista de códigos."""
    driver = iniciar_driver()
    driver.get("https://www.deltron.com.pe/login.php?prev=/index_2.php")
    input("Ingresa tus credenciales en el navegador y presiona Enter para continuar...")

    resultados = {}
    for codigo in codigos:
        precio_promo, promos_adicionales = buscar_promocion(driver, codigo)
        resultados[codigo] = (precio_promo, promos_adicionales)
        print(f"\nResultado parcial para {codigo}:")
        print(f"Precio Promoción: {precio_promo if precio_promo is not None else 'Sin promoción'}")
        print(f"Detalles Promoción: {'; '.join(promos_adicionales) if promos_adicionales else 'Ninguno'}")
        time.sleep(2)

    driver.quit()
    return resultados

if __name__ == "__main__":
    codigos_prueba = ["MON27CTE2731S", "SSDKTSA400S480G", "NBHP8U8B8LA", "NBLEN82TT00EALM"]
    resultados = probar_promocion(codigos_prueba)

    print("\nResultados de la prueba:")
    for codigo, (promo, detalles) in resultados.items():
        print(f"Código: {codigo}")
        print(f"Precio Promoción: {promo if promo is not None else 'Sin promoción'}")
        print(f"Detalles Promoción: {'; '.join(detalles) if detalles else 'Ninguno'}")