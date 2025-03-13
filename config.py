import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://HARD:Araza159753@localhost/tienda_tecnologia'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta para subir archivos (ruta absoluta)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # Clave secreta para Flask
    SECRET_KEY = 'Hard@159753'  # Cambia esto por una clave segura