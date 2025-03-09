import os
import pandas as pd
import csv
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import time

def process_chunk(args):
    """Procesa un chunk de códigos usando requests con reintentos y caché compartido."""
    codigos, cookies, progress_queue, total_codigos, process_index, cache = args
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resultados = []
    processed = 0
    chunk_size = len(codigos)
    
    start_time = time.time()
    for codigo in codigos:
        page_start = time.time()
        retries = 1
        for attempt in range(retries + 1):
            try:
                if codigo in cache:
                    print(f"Usando caché para {codigo}")
                    resultados.append(cache[codigo])
                    break
                
                url_producto = f"https://www.deltron.com.pe/modulos/productos/items/producto.php?item_number={codigo}"
                print(f"Procesando código: {codigo}")
                response = requests.get(url_producto, headers=headers, cookies=cookies, timeout=5)
                
                if response.status_code != 200:
                    raise Exception(f"Respuesta no válida: {response.status_code}")
                
                soup = BeautifulSoup(response.text, "html.parser")
                precios_secciones = soup.find_all(class_="product-price-discount")
                
                if not precios_secciones:
                    print(f"No se encontraron datos de promoción para {codigo}")
                    resultado = (None, [])
                    cache[codigo] = resultado
                    resultados.append(resultado)
                    break

                precio_promo_valor = None
                promociones_adicionales = []

                for seccion in precios_secciones:
                    try:
                        tipo_precio = seccion.find(class_="product-price-type")
                        if tipo_precio and "Precio Promoci" in tipo_precio.text.strip():
                            precio_promo_elem = seccion.find("b", class_="aqui1")
                            precio_promo = precio_promo_elem.text.strip()
                            precio_promo_valor = float(precio_promo.replace("US $", "").replace("+ IGV", "").strip())
                            print(f"Promoción encontrada para {codigo}: {precio_promo} (Valor: {precio_promo_valor})")
                    except:
                        pass

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
                    print(f"Sin precio promocional para {codigo}")
                if not promociones_adicionales:
                    print(f"Sin promociones adicionales para {codigo}")
                else:
                    print(f"Promociones adicionales para {codigo}: {promociones_adicionales}")

                resultado = (precio_promo_valor, promociones_adicionales)
                cache[codigo] = resultado
                resultados.append(resultado)
                break
            
            except Exception as e:
                if attempt < retries:
                    print(f"Reintentando {codigo} ({attempt + 1}/{retries}) tras error: {e}")
                    time.sleep(1)
                else:
                    print(f"Error final para {codigo}: {e}")
                    resultados.append((None, []))
                    break
        
        page_time = time.time() - page_start
        print(f"Tiempo para {codigo}: {page_time:.2f} segundos")
        processed += 1
        if progress_queue and total_codigos:
            progress = (processed + (process_index * chunk_size)) / total_codigos * 100
            progress_queue.put(progress)
    
    elapsed_time = time.time() - start_time
    print(f"Proceso {process_index} terminó en {elapsed_time:.2f} segundos para {chunk_size} códigos ({elapsed_time/chunk_size:.2f} s/código)")
    return resultados

def limpiar_csv(csv_file, output_file, cookies=None, progress_queue=None, cache=None):
    """Procesa el CSV con manejo de tamaño variable y depuración, aplicando reglas específicas."""
    try:
        start_time = time.time()
        if cache is None:
            cache = {}

        with open(csv_file, newline='', encoding='latin1') as f:
            data = csv.reader(f, delimiter=',')
            notes = list(data)
            if not notes or len(notes) < 2:
                print(f"Advertencia: '{csv_file}' está vacío o no tiene datos válidos")
                if progress_queue:
                    progress_queue.put(100)
                return cache
            
            notes = [row for row in notes if len(row) == 9 and row[0].strip() != '']
            if not notes:
                print(f"Advertencia: '{csv_file}' no tiene filas válidas")
                if progress_queue:
                    progress_queue.put(100)
                return cache
            
            header = notes.pop(0)
            notes.sort(key=lambda x: x[0])
            print(f"Procesando '{csv_file}' con {len(notes)} productos")

            custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", 
                            "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
            filtered_notes = []

            codigos = [row[1] for row in notes]
            num_processes = 4
            chunk_size = max(1, len(codigos) // num_processes)
            codigos_chunks = [codigos[i:i + chunk_size] for i in range(0, len(codigos), chunk_size)]

            with Pool(processes=num_processes) as pool:
                args = [(chunk, cookies, progress_queue, len(codigos), i, cache) for i, chunk in enumerate(codigos_chunks)]
                resultados = pool.map(process_chunk, args)

            resultados_flat = [item for sublist in resultados for item in sublist]
            for row, (precio_promo, promos_adicionales) in zip(notes, resultados_flat):
                # Procesar STOCK
                stock_raw = row[3].strip()
                if not stock_raw:  # Campo vacío
                    stock = 0
                elif stock_raw == ">20":  # Si es ">20"
                    stock = 20
                else:
                    try:
                        stock = int(float(stock_raw))  # Convertir a entero
                    except ValueError:
                        stock = 0  # Si no es numérico, 0

                # Procesar PRECIO DÓLARES
                precio_dolares = float(row[4]) if row[4].strip() else 0.0

                # Procesar PROMOCIÓN (formato contabilidad con $)
                if precio_promo is not None:
                    promocion = f"${precio_promo:.2f}"  # Formato con símbolo de dólares
                else:
                    promocion = ""  # Dejar vacío si no hay promoción

                detalle_promo = "; ".join(promos_adicionales) if promos_adicionales else ""
                filtered_notes.append([row[0], row[1], row[2], stock, precio_dolares, row[7], row[8], 
                                      promocion, detalle_promo])

            # Crear DataFrame y guardar
            df = pd.DataFrame(filtered_notes, columns=custom_header)
            df['STOCK'] = df['STOCK'].astype(int)  # Asegurar que STOCK sea entero
            df.to_csv(output_file, index=False, encoding='utf-8-sig')  # UTF-8 con BOM para compatibilidad
            
            elapsed_time = time.time() - start_time
            print(f"Archivo '{csv_file}' limpiado y guardado como '{output_file}' con {len(notes)} productos")
            print(f"Tiempo total de procesamiento: {elapsed_time:.2f} segundos ({elapsed_time/len(notes):.2f} s/producto)")
            print(f"Entradas en caché global: {len(cache)}")
            if progress_queue:
                progress_queue.put(100)

        return cache
    except Exception as e:
        import traceback
        print(f"Error al limpiar el archivo '{csv_file}': {str(e)}")
        print(traceback.format_exc())
        if progress_queue:
            progress_queue.put(100)
        return cache

if __name__ == "__main__":
    csv_file = "descargas/Lima - Principal.csv"
    output_file = "descargas/Lima - Principal_modificado.csv"
    cookies = {
        "_ga_WRF04X8D8W": "GS1.1.1741451771.1.0.1741451771.60.0.0",
        "_ga": "GA1.1.1330280944.1741451772",
        "clientinscrito": "20604503427%23548",
        "nivelmagic": "%25FF%25A7%25A7K%25B5%25C6%25E1Z%2591XQ3%25E7%25B1%2597%25CC%25A538%2599%25D54%2502%25E2%250A%25BB%25DC%25D5%2590%257B%25D7%25A4%25DA%258C%25C8%25BA%2514%258D%2503%2580S%257Fyu",
        "deltronlogin": "20604503427"
    }
    limpiar_csv(csv_file, output_file, cookies=cookies)