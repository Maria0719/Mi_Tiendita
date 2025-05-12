from app import app, db
from app.models import Gasto

with app.app_context():
    gastos = Gasto.query.all()
    print("💸 Gastos registrados:")
    for g in gastos:
        print(f"{g.id}: {g.descripcion} | Valor: ${g.valor}")
