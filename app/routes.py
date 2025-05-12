
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Product, Gasto
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Página de bienvenida
@app.route('/')
def inicio():
    grafica_demo = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABGoAAALv..."  # pega aquí el base64 completo que generé
    return render_template('inicio.html', grafica_demo=grafica_demo)


# Página principal de productos
@app.route('/index')
def index():
    products = Product.query.all()
    return render_template('index.html', productos=products)

# Agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            precio_compra = float(request.form['precio_compra'])
            ganancia_percent = float(request.form['ganancia'])
            stock = int(request.form['stock'])
            categoria = request.form['categoria']
            precio_venta = precio_compra * (1 + ganancia_percent / 100)

            nuevo_producto = Product(
                nombre=nombre,
                precio_compra=precio_compra,
                precio_venta=precio_venta,
                stock=stock,
                categoria=categoria
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ocurrió un error al agregar el producto: {e}', 'danger')
            return redirect(url_for('agregar'))
    return render_template('agregar.html')

# Editar producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = Product.query.get_or_404(id)
    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre']
            precio_compra = float(request.form['precio_compra'])
            ganancia_percent = float(request.form['ganancia'])
            producto.precio_compra = precio_compra
            producto.precio_venta = precio_compra * (1 + ganancia_percent / 100)
            producto.stock = int(request.form['stock'])
            producto.categoria = request.form['categoria']
            db.session.commit()
            flash('Producto actualizado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ocurrió un error al actualizar el producto: {e}', 'danger')
            return redirect(url_for('editar', id=id))
    return render_template('editar.html', producto=producto)

# Eliminar producto
@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Product.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('index'))

# Resumen de ganancias
@app.route('/ganancias')
def ganancias():
    productos = Product.query.all()
    gastos = Gasto.query.all()
    valor_total_compra = sum(p.precio_compra * p.stock for p in productos)
    valor_total_venta = sum(p.precio_venta * p.stock for p in productos)
    total_ganancia = valor_total_venta - valor_total_compra
    total_gastos = sum(g.valor for g in gastos)
    ganancia_final = total_ganancia - total_gastos

    return render_template('ganancias.html', 
                valor_compra_total=valor_total_compra, 
                valor_venta_total=valor_total_venta, 
                total_gastos=total_gastos, 
                ganancias_total=ganancia_final)

# Página de gráficas con 4 gráficos
@app.route('/graficas')
def graficas():
    productos = Product.query.all()
    gastos = Gasto.query.all()
    sns.set_style('whitegrid')

    # === Preparar DataFrame base ===
    datos_productos = []
    for p in productos:
        if p.precio_compra > 0:
            porcentaje = ((p.precio_venta - p.precio_compra) / p.precio_compra) * 100
        else:
            porcentaje = 0
        datos_productos.append({
            "nombre": p.nombre,
            "precio_compra": p.precio_compra,
            "precio_venta": p.precio_venta,
            "stock": p.stock,
            "categoria": p.categoria,
            "ganancia_porcentaje": porcentaje,
            "ganancia_total": (p.precio_venta - p.precio_compra) * p.stock
        })

    df = pd.DataFrame(datos_productos)
    total_gastos = sum(g.valor for g in gastos)
    ganancia_bruta = df["ganancia_total"].sum()
    ganancia_neta = ganancia_bruta - total_gastos

    # === Gráfica 1: Porcentaje de ganancia por producto ===
    fig1, ax1 = plt.subplots(figsize=(max(10, len(df) * 1.2), 6))
    sns.barplot(x="nombre", y="ganancia_porcentaje", data=df, ax=ax1, palette="Purples")
    ax1.set_ylim(0, 110)
    ax1.set_title("Porcentaje de Ganancia por Producto")
    ax1.set_ylabel("Ganancia (%)")
    ax1.set_xlabel("Producto")
    ax1.tick_params(axis='x', rotation=30)
    for i, row in df.iterrows():
        ax1.text(i, row["ganancia_porcentaje"] + 2, f'{row["ganancia_porcentaje"]:.0f}%', ha='center', fontsize=10)
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    grafica1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # === Gráfica 2: Resumen financiero ===
    df_finanzas = pd.DataFrame({
        "Categoría": ["Ganancia Bruta", "Gastos", "Ganancia Neta"],
        "Valor": [ganancia_bruta, total_gastos, ganancia_neta]
    })
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Categoría", y="Valor", data=df_finanzas, palette=["#4caf50", "#f44336", "#2196f3"], ax=ax2)
    ax2.set_title("Resumen Financiero")
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    grafica2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    # === Gráfica 3: Top 5 productos por valor de inventario ===
    df["valor_inventario"] = df["precio_compra"] * df["stock"]
    top5_inv = df.nlargest(5, "valor_inventario")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(x="valor_inventario", y="nombre", data=top5_inv, palette="Blues_d", ax=ax3)
    ax3.set_title("Top 5 Productos por Valor de Inventario")
    ax3.set_xlabel("Valor Total (Precio Compra × Stock)")
    ax3.set_ylabel("Producto")
    for i, v in enumerate(top5_inv["valor_inventario"]):
        ax3.text(v + 1000, i, f"${v:,.0f}", va='center')
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format='png')
    buf3.seek(0)
    grafica3 = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)

    # === Gráfica 4: Porcentaje de ganancia promedio por categoría ===
    df_categoria = df[df["precio_compra"] > 0].copy()
    df_categoria["ganancia_porcentaje"] = ((df_categoria["precio_venta"] - df_categoria["precio_compra"]) / df_categoria["precio_compra"]) * 100
    promedio_categoria = df_categoria.groupby("categoria")["ganancia_porcentaje"].mean().reset_index()
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(x="categoria", y="ganancia_porcentaje", data=promedio_categoria, palette="Purples_d", ax=ax4)
    ax4.set_title("Ganancia Promedio por Categoría")
    ax4.set_ylabel("Ganancia (%)")
    ax4.set_xlabel("Categoría")
    ax4.tick_params(axis='x', rotation=30)
    for i, row in promedio_categoria.iterrows():
        ax4.text(i, row["ganancia_porcentaje"] + 2, f"{row['ganancia_porcentaje']:.1f}%", ha='center')
    buf4 = io.BytesIO()
    fig4.savefig(buf4, format='png')
    buf4.seek(0)
    grafica4 = base64.b64encode(buf4.getvalue()).decode('utf-8')
    plt.close(fig4)

    return render_template("graficas.html", grafica1=grafica1, grafica2=grafica2, grafica3=grafica3, grafica4=grafica4)

# Listado de gastos
@app.route('/gastos')
def gastos():
    lista_gastos = Gasto.query.all()
    total = sum(g.valor for g in lista_gastos)
    return render_template('gastos.html', gastos=lista_gastos, total=total)

# Agregar gasto
@app.route('/agregar_gasto', methods=['GET', 'POST'])
def agregar_gasto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        valor = float(request.form['valor'])
        nuevo_gasto = Gasto(descripcion=descripcion, valor=valor)
        db.session.add(nuevo_gasto)
        db.session.commit()
        flash('Gasto agregado correctamente', 'success')
        return redirect(url_for('gastos'))
    return render_template('agregar_gasto.html')

# Editar gasto
@app.route('/editar_gasto/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    gasto = Gasto.query.get_or_404(id)
    if request.method == 'POST':
        gasto.descripcion = request.form['descripcion']
        gasto.valor = float(request.form['valor'])
        db.session.commit()
        flash('Gasto actualizado exitosamente!', 'success')
        return redirect(url_for('gastos'))
    return render_template('editar_gasto.html', gasto=gasto)

# Eliminar gasto
@app.route('/eliminar_gasto/<int:id>', methods=['POST'])
def eliminar_gasto(id):
    gasto = Gasto.query.get_or_404(id)
    db.session.delete(gasto)
    db.session.commit()
    flash('Gasto eliminado exitosamente!', 'success')
    return redirect(url_for('gastos'))

# Vista de resumen general combinando productos y gastos
@app.route('/resumen_general')
def resumen_general():
    productos = Product.query.all()
    gastos = Gasto.query.all()
    return render_template('resumen_general.html', productos=productos, gastos=gastos)
