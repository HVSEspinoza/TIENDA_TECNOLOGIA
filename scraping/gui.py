import sys
import os
# Ajusta el path para apuntar al directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from scraping.data_extraction import iniciar_sesion, extraer_datos, almacenes
from multiprocessing import Manager
import threading
import os
import csv
from scraping.data_cleaning import limpiar_csv
import time

print("Almacenes importados:", almacenes)

def iniciar_sesion_gui():
    driver = iniciar_sesion()
    messagebox.showinfo("Información", "Ingresa tus credenciales manualmente en la ventana del navegador y luego presiona 'OK'.")
    print("URL después del login:", driver.current_url)
    cookies = driver.get_cookies()
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    print("Cookies capturadas (diccionario):", cookies_dict)
    return driver, cookies_dict

def get_product_count(csv_file):
    try:
        with open(csv_file, newline='', encoding='latin1') as f:
            data = csv.reader(f, delimiter=',')
            notes = [row for row in data if len(row) == 9 and row[0].strip() != '']
            return len(notes) - 1
    except Exception as e:
        print(f"Error al contar productos en {csv_file}: {e}")
        return 0

def iniciar_programa_gui(root, driver, cookies, almacen_vars, progress_bar, progress_label, progress_queue, global_cache):
    if driver is not None and cookies is not None:
        def run_program():
            nonlocal driver  # Declarar driver como nonlocal al inicio
            global_cache.clear()
            print("Caché global limpiado al inicio de la ejecución.")
            selected_almacenes = {name: almacenes[name] for name, var in almacen_vars.items() if var.get()}
            if not selected_almacenes:
                messagebox.showwarning("Advertencia", "Selecciona al menos un almacén.")
                return

            url_almacenes = "https://www.deltron.com.pe/modulos/productos/listaprodnw.php"
            carpeta_descargas = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'downloads')
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'scraped_data')
            
            # Crear carpetas si no existen
            os.makedirs(carpeta_descargas, exist_ok=True)
            os.makedirs(base_dir, exist_ok=True)
            
            # Lista para almacenar almacenes que fallaron en la descarga
            almacenes_fallidos = []
            total_almacenes = len(selected_almacenes)
            processed_almacenes = 0

            # Primer intento para cada almacén
            for name, label in selected_almacenes.items():
                try:
                    print(f"Intento 1 de 2 para extraer datos del almacén: {label}")
                    # Limpiar carpeta de descargas antes de intentar
                    for file in os.listdir(carpeta_descargas):
                        os.remove(os.path.join(carpeta_descargas, file))
                    
                    # Extraer datos solo para este almacén
                    extraer_datos(url_almacenes, {name: label}, driver, carpeta_descargas, progress_queue)
                    
                    # Verificar si se creó una carpeta para este almacén en scraped_data
                    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f.startswith(f"{label}_")]
                    if folders:
                        print(f"Descarga exitosa para {label}: Carpeta creada en {base_dir}")
                    else:
                        print(f"No se descargó ningún CSV para {label} en el intento 1")
                        almacenes_fallidos.append((name, label))
                except Exception as e:
                    print(f"Error al extraer datos para {label} en intento 1: {e}")
                    almacenes_fallidos.append((name, label))
                
                processed_almacenes += 1
                if progress_queue:
                    progress = (processed_almacenes / total_almacenes) * 50
                    progress_queue.put(progress)

            # Segundo intento para almacenes que fallaron
            if almacenes_fallidos:
                print(f"Reintentando descarga para {len(almacenes_fallidos)} almacenes fallidos después de 5 segundos...")
                time.sleep(5)
                driver.get(url_almacenes)
                
                for name, label in almacenes_fallidos:
                    try:
                        print(f"Intento 2 de 2 para extraer datos del almacén: {label}")
                        # Limpiar carpeta de descargas antes de reintentar
                        for file in os.listdir(carpeta_descargas):
                            os.remove(os.path.join(carpeta_descargas, file))
                        
                        # Extraer datos solo para este almacén
                        extraer_datos(url_almacenes, {name: label}, driver, carpeta_descargas, progress_queue)
                        
                        # Verificar si se creó una carpeta para este almacén en scraped_data
                        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f.startswith(f"{label}_")]
                        if folders:
                            print(f"Descarga exitosa para {label} en reintento: Carpeta creada en {base_dir}")
                        else:
                            print(f"No se descargó ningún CSV para {label} en el intento 2")
                    except Exception as e:
                        print(f"Error al extraer datos para {label} en intento 2: {e}")
                    
                    processed_almacenes += 1
                    if progress_queue:
                        progress = (processed_almacenes / total_almacenes) * 50
                        progress_queue.put(progress)

            # Verificar si hay CSVs para procesar
            csv_info = []
            print(f"Buscando CSVs en {base_dir}")
            for folder in os.listdir(base_dir):
                folder_path = os.path.join(base_dir, folder)
                if os.path.isdir(folder_path):
                    almacen_name = folder.split('_')[0]
                    if almacen_name in selected_almacenes.values():
                        for file in os.listdir(folder_path):
                            if file.endswith(".csv") and not file.endswith("_modificado.csv"):
                                csv_file = os.path.join(folder_path, file)
                                output_file = csv_file.replace(".csv", "_modificado.csv")
                                product_count = get_product_count(csv_file)
                                csv_info.append((csv_file, output_file, cookies, product_count))
                                print(f"Encontrado CSV: {csv_file}, productos: {product_count}")

            if not csv_info:
                print("No se encontraron CSVs para procesar. Revisa la extracción.")
                progress_queue.put(100)
                return

            csv_info_sorted = sorted(csv_info, key=lambda x: x[3])
            total_products = sum(info[3] for info in csv_info_sorted)
            processed_products = 0

            print(f"Total de productos a procesar: {total_products}")
            for csv_file, output_file, cookies_local, product_count in csv_info_sorted:
                print(f"Procesando {csv_file} con {product_count} productos")
                try:
                    limpiar_csv(csv_file, output_file, cookies=cookies_local, progress_queue=progress_queue, cache=global_cache)
                    processed_products += product_count
                    progress = 50 + (processed_products / total_products) * 50
                    progress_queue.put(progress)
                    print(f"Progreso actualizado a {progress:.1f}%")
                except Exception as e:
                    print(f"Error en limpiar_csv para {csv_file}: {e}")
            
            print(f"Procesamiento de todos los almacenes completado con {len(global_cache)} entradas en caché global.")

        def update_progress():
            while True:
                try:
                    progress = progress_queue.get(timeout=1)
                    progress_bar.config(value=progress)
                    progress_label.config(text=f"Procesando: {progress:.1f}%")
                    if progress >= 100:
                        progress_label.config(text="Procesamiento completado: 100%")
                        driver.quit()
                        break
                except:
                    root.after(100, update_progress)
                    break

        # Iniciar el hilo sin pasar driver como argumento, ya que usamos nonlocal
        threading.Thread(target=run_program, daemon=True).start()
        update_progress()
    else:
        print("Error: Driver o cookies no están definidos. Inicia sesión primero.")

def main():
    root = tk.Tk()
    root.title("Descargador de Datos de Deltron")
    root.geometry("400x600")
    
    driver = None
    cookies = None
    manager = Manager()
    progress_queue = manager.Queue()
    global_cache = manager.dict()
    
    def set_driver_and_cookies():
        nonlocal driver, cookies
        driver, cookies = iniciar_sesion_gui()

    frame_almacenes = tk.Frame(root)
    frame_almacenes.pack(pady=20)
    label_almacenes = tk.Label(frame_almacenes, text="Selecciona los almacenes:")
    label_almacenes.pack(pady=10)
    almacen_vars = {}
    print("Generando checkboxes con almacenes:", almacenes)
    for name, label in almacenes.items():
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame_almacenes, text=label, variable=var)
        checkbox.pack(anchor='w')
        almacen_vars[name] = var
    
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=20)
    button_login = tk.Button(frame_botones, text="Iniciar Sesión", command=set_driver_and_cookies)
    button_login.pack(side='left', padx=10)
    button_iniciar = tk.Button(frame_botones, text="Iniciar", 
                              command=lambda: iniciar_programa_gui(root, driver, cookies, almacen_vars, progress_bar, progress_label, progress_queue, global_cache))
    button_iniciar.pack(side='right', padx=10)
    
    frame_progress = tk.Frame(root)
    frame_progress.pack(pady=20)
    progress_label = tk.Label(frame_progress, text="Procesando: 0%")
    progress_label.pack()
    progress_bar = ttk.Progressbar(frame_progress, length=300, mode='determinate', maximum=100)
    progress_bar.pack()

    root.mainloop()

if __name__ == "__main__":
    main()