import pandas as pd
from app import db, Producto

def cargar_csv_a_bd(csv_file, almacen_id):
    try:
        data = pd.read_csv(csv_file, encoding='latin1', delimiter=',', on_bad_lines='skip')
        print(f"Encabezados del archivo {csv_file}: {data.columns}")

        if 'codigo' not in data.columns or 'descripcion' not in data.columns or 'stock' not in data.columns or 'precio_usd' not in data.columns or 'categoria' not in data.columns:
            print(f"El archivo {csv_file} no contiene los encabezados esperados.")
            return
        
        Producto.query.filter_by(almacen_id=almacen_id).delete()
        for index, row in data.iterrows():
            nuevo_producto = Producto(
                nombre=row.get('descripcion', 'sin_nombre'),
                precio=row.get('precio_usd', 0),
                cantidad=row.get('stock', 0),
                almacen_id=almacen_id,
                categoria=row.get('categoria', 'sin_categoria')
            )
            db.session.add(nuevo_producto)
        db.session.commit()
        print(f"Datos del archivo {csv_file} cargados correctamente en la base de datos.")
    except Exception as e:
        print(f"Error al procesar el archivo '{csv_file}': {e}")
