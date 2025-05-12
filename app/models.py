from app import db
# Importa la instancia de SQLAlchemy ya configurada desde el módulo principal (app/__init__.py)

# ===========================
# Modelo Product (Tabla: products)
# ===========================
class Product(db.Model):
    __tablename__ = 'products'
    # Nombre explícito de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    # Columna ID: clave primaria, tipo entero, autoincremental

    nombre = db.Column(db.String(100), nullable=False)
    # Columna para el nombre del producto, tipo texto (hasta 100 caracteres), no puede estar vacía

    precio_compra = db.Column(db.Float, nullable=False)
    # Precio de compra del producto, tipo flotante (decimal), obligatorio

    precio_venta = db.Column(db.Float, nullable=False)
    # Precio de venta del producto, tipo flotante, obligatorio

    stock = db.Column(db.Integer, nullable=False)
    # Cantidad disponible en inventario, tipo entero, obligatorio

    categoria = db.Column(db.String(50))
    # Categoría del producto, texto opcional de hasta 50 caracteres

    def __repr__(self):
        return f"<Product {self.nombre}>"
    # Representación textual útil para depuración o consola interactiva

# ===========================
# Modelo Gasto (Tabla: gastos)
# ===========================
class Gasto(db.Model):
    __tablename__ = 'gastos'
    # Nombre explícito de la tabla

    id = db.Column(db.Integer, primary_key=True)
    # ID único para cada gasto, clave primaria

    descripcion = db.Column(db.String(200), nullable=False)
    # Texto descriptivo del gasto (obligatorio)

    valor = db.Column(db.Float, nullable=False)
    # Monto del gasto, tipo decimal (flotante), obligatorio

    def __repr__(self):
        return f"<Gasto {self.descripcion}: ${self.valor}>"
    # Representación amigable del gasto (para consola/logs)
