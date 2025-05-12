
# 📦 MiTiendita

**MiTiendita** es una aplicación web desarrollada con **Flask** y **PostgreSQL**, diseñada para gestionar productos, registrar gastos y visualizar las ganancias de una tienda. La aplicación incluye interfaz de usuario, reportes visuales con gráficos y se puede ejecutar fácilmente con Docker.

---

## 🚀 Características principales

- ✅ Registro, edición y eliminación de productos.
- ✅ Registro y control de gastos.
- ✅ Visualización de ganancias totales (con y sin gastos).
- 📊 Gráficas dinámicas de rentabilidad con Seaborn y Matplotlib.
- 🐳 Listo para producción con Docker y Gunicorn.
- 🎨 Interfaz moderna, responsiva y fácil de usar.

---

## 🌐 Vistas de la aplicación

| Página | Descripción |
|-------|-------------|
| `/` | Página de bienvenida con logo, descripción de la app y botón de inicio. |
| `/index` | Lista de productos con detalles como precios, stock, ganancia total y opciones para editar/eliminar. |
| `/agregar` | Formulario para agregar nuevos productos calculando automáticamente el precio de venta según un porcentaje de ganancia. |
| `/editar/<id>` | Permite modificar la información de un producto existente. |
| `/gastos` | Lista de todos los gastos registrados, con total acumulado y opciones para editar/eliminar. |
| `/agregar_gasto` | Formulario para añadir nuevos gastos. |
| `/editar_gasto/<id>` | Edición de un gasto existente. |
| `/ganancias` | Muestra un resumen financiero con valor total de compra, venta, gastos y ganancia neta. |
| `/graficas` | Visualiza gráficas de porcentaje de ganancia por producto y resumen financiero. |

---

## 🧱 Estructura del proyecto

```
mi_tiendita/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── filters.py
│   ├── templates/
│   │   ├── inicio.html
│   │   ├── index.html
│   │   ├── agregar.html
│   │   ├── editar.html
│   │   ├── gastos.html
│   │   ├── agregar_gasto.html
│   │   ├── editar_gasto.html
│   │   ├── ganancias.html
│   │   └── graficas.html
│   └── static/
│       ├── style.css
│       └── logo.png
├── crear_tabla.py
├── run.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## ⚙️ Instalación local

### 🔧 Requisitos

- Python 3.9+
- PostgreSQL
- Docker y Docker Compose (opcional pero recomendado)

### 🔌 Configuración sin Docker

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar URI de PostgreSQL en app/__init__.py

# Crear tablas
python crear_tabla.py

# Ejecutar app
python run.py
```

Abrir en navegador: [http://localhost:5000](http://localhost:5000)

### 🐳 Con Docker

```bash
docker-compose up --build
```

Acceder a: [http://localhost:5002](http://localhost:5002)

---

## 📷 Capturas de Pantalla (sugeridas)

- Vista de bienvenida con logo animado
- Lista de productos y cálculo automático de ganancias
- Formularios para agregar productos y gastos
- Gráficas de ganancia por producto y resumen financiero

---

## 🧠 Tecnologías usadas

- Python 3.11
- Flask 3.1
- PostgreSQL
- SQLAlchemy
- Matplotlib & Seaborn
- Bootstrap 5
- Docker & Gunicorn

---

## 👨‍💻 Autor

Desarrollado con ❤️ por [MARIA JOSE RAMIREZ MONTERO]

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
