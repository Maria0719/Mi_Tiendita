from app import app, db
from app.models import Product, Gasto  # Importa ambos modelos

with app.app_context():
    try:
        db.create_all()
        print("✅ Tablas 'products' y 'gastos' creadas correctamente.")
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
