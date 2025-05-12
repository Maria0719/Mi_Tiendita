from flask import Flask
# Importa la clase Flask, que es la base de toda aplicación Flask

from flask_sqlalchemy import SQLAlchemy
# Importa SQLAlchemy, el ORM (Object-Relational Mapper) que permite interactuar con la base de datos de forma más simple

app = Flask(__name__)
# Crea una instancia de la aplicación Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tiendita_jm61_user:xstC4ioYv3LTZHTUMCjIJGbtSJ0sCr49@dpg-d0balv95pdvs73cgr1l0-a.oregon-postgres.render.com/tiendita_jm61'
# Configura la URI de conexión a la base de datos PostgreSQL alojada en Render

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Desactiva el rastreo de modificaciones de objetos (ahorra recursos del sistema)

app.secret_key = 'mitiendita-2025'
# Clave secreta de la aplicación, usada por Flask para sesiones, mensajes flash, protección CSRF, etc.

db = SQLAlchemy(app)
# Crea una instancia de SQLAlchemy conectada a la app para gestionar modelos y sesiones de base de datos

from app import routes, filters
# Importa los módulos `routes.py` y `filters.py` para que Flask reconozca las rutas y los filtros definidos allí
# Esta línea se coloca al final para evitar problemas de importación circular
