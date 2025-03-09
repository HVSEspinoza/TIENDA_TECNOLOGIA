import tkinter as tk
from tkinter import messagebox, ttk
from data_extraction import iniciar_sesion, extraer_datos, almacenes
from multiprocessing import Manager
import threading
import os
import csv
from data_cleaning import limpiar_csv
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
            carpeta_descargas = os.path.abspath("descargas")
            
            # Extraer datos con reintentos
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"Intento {attempt + 1} de {max_retries} para extraer datos.")
                    extraer_datos(url_almacenes, selected_almacenes, driver, carpeta_descargas, progress_queue)
                    break
                except Exception as e:
                    print(f"Error en intento {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        try:
                            driver.get("https://www.deltron.com.pe")
                            print("Reconexión exitosa al sitio.")
                        except:
                            print("No se pudo reconectar. Reiniciando driver.")
                            driver.quit()
                            driver, new_cookies = iniciar_sesion_gui()  # Reiniciar driver y cookies
                            cookies.update(new_cookies)  # Actualizar cookies
                    else:
                        print("Todos los intentos fallaron. Algunos CSVs pueden estar incompletos.")

            base_dir = "C:/Users/CORPORACION ARAZA/Desktop/tienda_tecnologia/productos_deltron"
            csv_info = []
            print(f"Buscando CSVs en {base_dir}")
            for folder in os.listdir(base_dir):
                folder_path = os.path.join(base_dir, folder)
                if os.path.isdir(folder_path):
                    almacen_name = folder.split('_')[0]
                    print(f"Procesando carpeta: {folder}, nombre del almacén: {almacen_name}")
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