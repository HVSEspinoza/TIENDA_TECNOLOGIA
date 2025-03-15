import pandas as pd
import csv
import unicodedata

# Ruta del CSV a inspeccionar
csv_file_path = r"C:\Users\CORPORACION ARAZA\Desktop\tienda_tecnologia\uploads\Cusco_2025-03-08_18-53-39_DCW_20250308065338_modificado.csv"

# Encabezados esperados (según tu código)
custom_header = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA", "PROMOCIÓN", "DETALLE PROMOCIÓN"]
required_columns = ["CATEGORÍA", "CÓDIGO", "DESCRIPCIÓN", "STOCK", "PRECIO DÓLARES", "GARANTÍA", "MARCA"]

# Función para normalizar encabezados (como en helpers.py)
def normalize_header(col):
    return unicodedata.normalize('NFKD', col.strip()).encode('ASCII', 'ignore').decode('ASCII').upper()

def inspect_csv():
    print(f"\nInspeccionando el archivo: {csv_file_path}\n")

    # 1. Leer el CSV con pandas para obtener los encabezados
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8-sig', delimiter=',', on_bad_lines='skip')
        print("Encabezados detectados (sin normalizar):")
        print(df.columns.tolist())

        # Normalizar los encabezados
        normalized_columns = [normalize_header(col) for col in df.columns]
        print("\nEncabezados normalizados (como los procesa el código):")
        print(normalized_columns)

        # Verificar si las columnas requeridas están presentes
        custom_header_normalized = [normalize_header(col) for col in custom_header]
        required_columns_normalized = [normalize_header(col) for col in required_columns]

        print("\nEncabezados esperados (normalizados):")
        print(custom_header_normalized)

        missing_required = [col for col in required_columns_normalized if col not in normalized_columns]
        if missing_required:
            print("\n¡Error! Faltan columnas requeridas:")
            print(missing_required)
        else:
            print("\nTodas las columnas requeridas están presentes.")

        # 2. Mostrar las primeras 5 filas para verificar los datos
        print("\nPrimeras 5 filas del CSV:")
        print(df.head().to_string())

    except Exception as e:
        print(f"Error al leer el CSV con pandas: {e}")

    # 3. Leer el CSV con csv.reader para inspeccionar los encabezados crudos
    print("\nLeyendo el CSV con csv.reader (encabezados crudos):")
    try:
        with open(csv_file_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)  # Leer la primera fila (encabezados)
            print("Encabezados crudos (incluyendo posibles caracteres invisibles):")
            print([f"'{header}'" for header in headers])

            # Mostrar las primeras 5 filas de datos (excluyendo el encabezado)
            print("\nPrimeras 5 filas de datos (excluyendo el encabezado):")
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                print(row)

    except Exception as e:
        print(f"Error al leer el CSV con csv.reader: {e}")

if __name__ == "__main__":
    inspect_csv()