from app import app, db
from app.models import Product

with app.app_context():
    productos = Product.query.all()
    print(" Productos registrados:")
    for p in productos:
        print(f"{p.id}: {p.nombre} | Compra: ${p.precio_compra} | Venta: ${p.precio_venta} | Stock: {p.stock} | Categoría: {p.categoria}")
