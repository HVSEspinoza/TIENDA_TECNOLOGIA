import requests
from bs4 import BeautifulSoup
import time

def buscar_promocion(cookies, headers, codigo):
    """Accede a la página del producto con requests y extrae precio promocional y promociones adicionales."""
    try:
        url_producto = f"https://www.deltron.com.pe/modulos/productos/items/producto.php?item_number={codigo}"
        print(f"Accediendo a la página del producto: {url_producto}")
        
        start_time = time.time()
        response = requests.get(url_producto, headers=headers, cookies=cookies, timeout=5)
        print(f"Estado de la solicitud: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        precios_secciones = soup.find_all(class_="product-price-discount")
        
        if not precios_secciones:
            print("No se encontraron elementos con clase 'product-price-discount'.")
            return None, []

        precio_promo_valor = None
        promociones_adicionales = []

        for seccion in precios_secciones:
            html_seccion = str(seccion)
            print(f"Sección: {html_seccion}")

            try:
                tipo_precio = seccion.find(class_="product-price-type")
                if tipo_precio:
                    texto_precio = tipo_precio.text.strip()
                    print(f"Texto encontrado en product-price-type: '{texto_precio}'")
                    if "Precio Promoci" in texto_precio:
                        precio_promo_elem = seccion.find("b", class_="aqui1")
                        precio_promo = precio_promo_elem.text.strip()
                        precio_promo_valor = float(precio_promo.replace("US $", "").replace("+ IGV", "").strip())
                        print(f"Promoción encontrada: {precio_promo} (Valor: {precio_promo_valor})")
            except Exception as e:
                print(f"Error al buscar precio promocional: {e}")

            try:
                promo_elem = seccion.find(attrs={"data-promo": True})
                if promo_elem:
                    promo_id = promo_elem["data-promo"]
                    promo_texto = promo_elem.find("img")["title"].strip()
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

        elapsed_time = time.time() - start_time
        print(f"Tiempo para {codigo}: {elapsed_time:.2f} segundos")
        return precio_promo_valor, promociones_adicionales

    except Exception as e:
        print(f"Error general al buscar promoción para {codigo}: {e}")
        return None, []

def probar_promocion(codigos):
    """Prueba la funcionalidad de búsqueda de promociones usando requests tras login manual."""
    print("Usando cookies capturadas manualmente del login en Selenium.")
    
    cookies = {
        "_ga_WRF04X8D8W": "GS1.1.1741451771.1.0.1741451771.60.0.0",
        "_ga": "GA1.1.1330280944.1741451772",
        "clientinscrito": "20604503427%23548",
        "nivelmagic": "%25FF%25A7%25A7K%25B5%25C6%25E1Z%2591XQ3%25E7%25B1%2597%25CC%25A538%2599%25D54%2502%25E2%250A%25BB%25DC%25D5%2590%257B%25D7%25A4%25DA%258C%25C8%25BA%2514%258D%2503%2580S%257Fyu",
        "deltronlogin": "20604503427"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    resultados = {}
    for codigo in codigos:
        precio_promo, promos_adicionales = buscar_promocion(cookies, headers, codigo)
        resultados[codigo] = (precio_promo, promos_adicionales)
        print(f"\nResultado parcial para {codigo}:")
        print(f"Precio Promoción: {precio_promo if precio_promo is not None else 'Sin promoción'}")
        print(f"Detalles Promoción: {'; '.join(promos_adicionales) if promos_adicionales else 'Ninguno'}")

    return resultados

if __name__ == "__main__":
    codigos_prueba = ["MON27CTE2731S", "SSDKTSA400S480G", "NBHP8U8B8LA", "NBLEN82TT00EALM"]
    resultados = probar_promocion(codigos_prueba)

    print("\nResultados de la prueba:")
    for codigo, (promo, detalles) in resultados.items():
        print(f"Código: {codigo}")
        print(f"Precio Promoción: {promo if promo is not None else 'Sin promoción'}")
        print(f"Detalles Promoción: {'; '.join(detalles) if detalles else 'Ninguno'}")