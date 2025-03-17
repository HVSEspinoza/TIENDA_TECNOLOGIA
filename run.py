import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app'))

from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes import init_routes
from app.config.settings import Config

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'templates')
static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static')
print(f"Buscando plantillas en: {template_dir}")
print(f"Buscando archivos estáticos en: {static_dir}")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)  # Añade static_folder aquí
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)