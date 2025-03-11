from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Almacen(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio_dolares = db.Column(db.Numeric(10, 2), nullable=False)
    precio_soles = db.Column(db.Numeric(10, 2), nullable=False)
    garantia = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    promocion = db.Column(db.Numeric(10, 2), nullable=True)
    detalle_promocion = db.Column(db.String(255), nullable=True)
    almacen_id = db.Column(db.String(100), db.ForeignKey('almacen.id'))

class ArchivoProcesado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    procesado = db.Column(db.Boolean, default=False)