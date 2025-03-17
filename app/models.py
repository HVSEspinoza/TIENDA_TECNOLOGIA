from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

db = SQLAlchemy()

class Almacen(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nombre

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio_compra_usd = db.Column(db.Numeric(10, 2), nullable=False)
    precio_compra_soles = db.Column(db.Numeric(10, 2), nullable=False)
    precio_oferta_compra_usd = db.Column(db.Numeric(10, 2), nullable=True)
    precio_oferta_compra_soles = db.Column(db.Numeric(10, 2), nullable=True)
    garantia = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)  # Categoría original del CSV
    categoria_general = db.Column(db.String(255), nullable=True)  # Nueva categoría general
    subcategoria = db.Column(db.String(255), nullable=True)  # Nueva subcategoría
    detalle_promocion = db.Column(db.String(255), nullable=True)
    almacen_id = db.Column(db.String(100), db.ForeignKey('almacen.id'))
    # Agregar la relación
    almacen = db.relationship('Almacen', backref='productos')

    @property
    def precio_venta_soles(self):
        return self.precio_compra_soles / Decimal('0.87') if self.precio_compra_soles else 0

    @property
    def precio_venta_oferta_soles(self):
        return self.precio_oferta_compra_soles / Decimal('0.87') if self.precio_oferta_compra_soles else 0

    # Cálculos para Precio de Venta al Público
    @property
    def margen_bruto_normal(self):
        return self.precio_venta_soles - self.precio_compra_soles if self.precio_venta_soles > 0 else 0

    @property
    def igv_a_pagar_normal(self):
        igv_cobrado = (self.precio_venta_soles * Decimal('0.18')) / Decimal('1.18')
        igv_pagado = (self.precio_compra_soles * Decimal('0.18')) / Decimal('1.18')
        return (igv_cobrado - igv_pagado) if (igv_cobrado - igv_pagado) > 0 else 0

    @property
    def impuesto_renta_normal(self):
        return self.precio_venta_soles * Decimal('0.01') if self.precio_venta_soles > 0 else 0

    @property
    def costo_tarjeta_credito_normal(self):
        return self.precio_venta_soles * Decimal('0.05') if self.precio_venta_soles > 0 else 0

    @property
    def utilidad_por_unidad_normal(self):
        gastos_operativos = self.igv_a_pagar_normal + self.impuesto_renta_normal + self.costo_tarjeta_credito_normal
        return self.margen_bruto_normal - gastos_operativos if self.margen_bruto_normal > 0 else 0

    # Cálculos para Precio Oferta de Venta
    @property
    def margen_bruto_oferta(self):
        return self.precio_venta_oferta_soles - self.precio_oferta_compra_soles if self.precio_venta_oferta_soles > 0 else 0

    @property
    def igv_a_pagar_oferta(self):
        if self.precio_venta_oferta_soles == 0:
            return 0
        igv_cobrado = (self.precio_venta_oferta_soles * Decimal('0.18')) / Decimal('1.18')
        igv_pagado = (self.precio_oferta_compra_soles * Decimal('0.18')) / Decimal('1.18')
        return (igv_cobrado - igv_pagado) if (igv_cobrado - igv_pagado) > 0 else 0

    @property
    def impuesto_renta_oferta(self):
        return self.precio_venta_oferta_soles * Decimal('0.01') if self.precio_venta_oferta_soles > 0 else 0

    @property
    def costo_tarjeta_credito_oferta(self):
        return self.precio_venta_oferta_soles * Decimal('0.05') if self.precio_venta_oferta_soles > 0 else 0

    @property
    def utilidad_por_unidad_oferta(self):
        if self.precio_venta_oferta_soles == 0:
            return 0
        gastos_operativos = self.igv_a_pagar_oferta + self.impuesto_renta_oferta + self.costo_tarjeta_credito_oferta
        return self.margen_bruto_oferta - gastos_operativos if self.margen_bruto_oferta > 0 else 0

    def __str__(self):
        return self.descripcion

class ArchivoProcesado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    procesado = db.Column(db.Boolean, default=False)