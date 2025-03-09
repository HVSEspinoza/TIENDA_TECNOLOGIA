from data_extraction import iniciar_sesion, extraer_datos
from app import app, Almacen
import os
import csv
from data_cleaning import limpiar_csv

# Usar la misma lista de almacenes que data_extraction.py
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

def iniciar_programa(driver, cookies, almacen_vars, progress_queue, global_cache):
    url_almacenes = "https://www.deltron.com.pe/modulos/productos/listaprodnw.php"
    almacenes_seleccionados = {name: almacenes[name] for name, var in almacen_vars.items() if var.get()}
    if not almacenes_seleccionados:
        print("Por favor, selecciona al menos un almacén.")
        return

    carpeta_descargas = os.path.abspath("descargas")
    print(f"Carpeta de descargas: {carpeta_descargas}")
    if driver:
        # Extraer datos de los almacenes seleccionados
        extraer_datos(url_almacenes, almacenes_seleccionados, driver, carpeta_descargas, progress_queue)
        
        with app.app_context():
            carpeta_base = os.path.abspath("productos_deltron")
            print(f"Carpeta base: {carpeta_base}")
            
            # Contar total de productos para un progreso más granular
            csv_info = []
            for root, dirs, files in os.walk(carpeta_base):
                for archivo in files:
                    if archivo.endswith('.csv') and not archivo.endswith('_modificado.csv'):
                        csv_file = os.path.join(root, archivo)
                        label = os.path.basename(root).split('_')[0]
                        output_file = os.path.join(root, f"{label}_modificado.csv")
                        product_count = len([row for row in csv.reader(open(csv_file, encoding='latin1')) 
                                           if len(row) == 9 and row[0].strip() != '']) - 1
                        csv_info.append((csv_file, output_file, product_count))
            
            total_productos = sum(info[2] for info in csv_info)
            processed_productos = 0
            print(f"Total de productos a procesar: {total_productos}")

            if not csv_info:
                print("No se encontraron CSVs para procesar.")
                progress_queue.put(100)
                return

            for csv_file, output_file, product_count in csv_info:
                try:
                    limpiar_csv(csv_file, output_file, cookies=cookies, progress_queue=progress_queue, cache=global_cache)
                    processed_productos += product_count
                    progress = (processed_productos / total_productos) * 100 if total_productos > 0 else 100
                    progress_queue.put(progress)
                    print(f"Archivo '{csv_file}' procesado y guardado como '{output_file}'")
                except Exception as e:
                    print(f"Error al procesar {csv_file}: {e}")
            
            print(f"Ejecución completada con {processed_productos} productos procesados y {len(global_cache)} entradas en caché global")
        
        driver.quit()