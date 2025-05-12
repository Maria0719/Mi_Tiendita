# filters.py
# Archivo que contiene filtros personalizados para usarlos en las plantillas HTML de Jinja2

from app import app
# Importa la instancia de la aplicación Flask desde el paquete 'app'

@app.template_filter('money')
# Define un filtro personalizado de plantilla llamado 'money', que se podrá usar como: {{ valor | money }}

def money_format(value):
    # Función que da formato monetario a un número
    try:
        return "${:,.0f}".format(value or 0).replace(",", ".")
        # Aplica formato:
        # - {:,.0f} → separa miles con comas y redondea a 0 decimales
        # - .replace(",", ".") → reemplaza comas por puntos para estilo latinoamericano
        # - value or 0 → usa 0 si el valor es None o 0
    except:
        return "$0"
        # Si ocurre algún error (por ejemplo, si value no es numérico), devuelve "$0"
