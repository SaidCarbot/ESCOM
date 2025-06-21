from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
import psycopg2
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración de la base de datos (ajusta según tu configuración)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '1234',
    'dbname': 'inventario',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Decorador para rutas que requieren autenticación
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('Por favor inicia sesión primero.', 'danger')
                return redirect(url_for('login'))
            if role and session['user']['rol'] != role:
                flash('No tienes permisos para acceder a esta página.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s;", (correo,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario[3].encode('utf-8')):
            session['user'] = {
                'id': usuario[0],
                'nombre': usuario[1],
                'correo': usuario[2],
                'rol': usuario[4]
            }
            flash(f'Bienvenido {usuario[1]}!', 'success')
            if usuario[4] == 'cliente':
                return redirect(url_for('cliente_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        rol = request.form['rol']
        
        if rol not in ['vendedor', 'cliente']:
            flash('Rol no válido', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, correo, contraseña, rol) VALUES (%s, %s, %s, %s);",
                (nombre, correo, hashed_password.decode('utf-8'), rol)
            )
            conn.commit()
            flash('Registro exitoso! Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()
    
    return render_template('register.html')

@app.route('/cliente')
@login_required(role='cliente')
def cliente_dashboard():
    return render_template('cliente.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

##################################

# ... (código anterior se mantiene igual)

# Ruta del dashboard de administrador
@app.route('/admin/dashboard')
@login_required(role='vendedor')
def admin_dashboard():
    return render_template('admin/dashboard.html', user=session['user'])

# Ruta para agregar producto
@app.route('/admin/agregar_producto', methods=['GET', 'POST'])
@login_required(role='vendedor')
def agregar_producto():
    if request.method == 'POST':
        # Procesar formulario de agregar producto
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        categoria_id = int(request.form['categoria_id'])
        fecha_caducidad = request.form['fecha_caducidad'] or None
        codigo_barras = request.form['codigo_barras'] or None
        costo_compra = float(request.form['costo_compra']) if request.form['costo_compra'] else None

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
            INSERT INTO Productos (nombre, descripcion, precio, stock, usuario_id, categoria_id, 
                                 fecha_de_caducidad, codigo_de_barras, costo_de_compra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (nombre, descripcion, precio, stock, session['user']['id'], 
                              categoria_id, fecha_caducidad, codigo_barras, costo_compra))
            conn.commit()
            flash('Producto agregado exitosamente!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()

    # Categorías para el formulario
    categorias = [
        (1, "Electrónica"), (2, "Ropa"), (3, "Calzado"), (4, "Comida y Bebidas"),
        (5, "Hogar"), (6, "Muebles"), (7, "Juguetes"), (8, "Deportes y Fitness"),
        (9, "Salud y Belleza"), (10, "Libros y Papelería"), (11, "Tecnología"),
        (12, "Jardinería y Exteriores"), (13, "Automotriz"), (14, "Accesorios"),
        (15, "Arte y Manualidades")
    ]
    
    return render_template('admin/agregar_producto.html', categorias=categorias)

# Ruta para actualizar producto
@app.route('/admin/actualizar_producto', methods=['GET', 'POST'])
@login_required(role='vendedor')
def actualizar_producto():
    if request.method == 'POST':
        # Procesar formulario de actualización
        producto_id = int(request.form['producto_id'])
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        categoria_id = int(request.form['categoria_id'])
        fecha_caducidad = request.form['fecha_caducidad'] or None
        codigo_barras = request.form['codigo_barras'] or None
        costo_compra = float(request.form['costo_compra']) if request.form['costo_compra'] else None

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
            UPDATE Productos 
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, 
                categoria_id = %s, fecha_de_caducidad = %s, 
                codigo_de_barras = %s, costo_de_compra = %s
            WHERE producto_id = %s AND usuario_id = %s
            """
            cur.execute(query, (nombre, descripcion, precio, stock, categoria_id, 
                              fecha_caducidad, codigo_barras, costo_compra, 
                              producto_id, session['user']['id']))
            conn.commit()
            flash('Producto actualizado exitosamente!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()

    # Obtener lista de productos para seleccionar
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT producto_id, nombre FROM Productos 
    WHERE usuario_id = %s ORDER BY producto_id DESC
    """, (session['user']['id'],))
    productos = cur.fetchall()
    cur.close()
    conn.close()

    # Categorías para el formulario
    categorias = [
        (1, "Electrónica"), (2, "Ropa"), (3, "Calzado"), (4, "Comida y Bebidas"),
        (5, "Hogar"), (6, "Muebles"), (7, "Juguetes"), (8, "Deportes y Fitness"),
        (9, "Salud y Belleza"), (10, "Libros y Papelería"), (11, "Tecnología"),
        (12, "Jardinería y Exteriores"), (13, "Automotriz"), (14, "Accesorios"),
        (15, "Arte y Manualidades")
    ]
    
    return render_template('admin/actualizar_producto.html', productos=productos, categorias=categorias)

# Ruta para ver productos
@app.route('/admin/ver_productos')
@login_required(role='vendedor')
def ver_productos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.producto_id, p.nombre, p.descripcion, p.precio, p.stock, 
           c.nombre as categoria, p.fecha_de_caducidad, 
           p.codigo_de_barras, p.costo_de_compra
    FROM Productos p
    JOIN Categorias c ON p.categoria_id = c.categoria_id
    WHERE p.usuario_id = %s
    """, (session['user']['id'],))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('admin/ver_productos.html', productos=productos)

# Ruta para eliminar producto
@app.route('/admin/eliminar_producto', methods=['GET', 'POST'])
@login_required(role='vendedor')
def eliminar_producto():
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Verificar que el producto pertenece al usuario
            cur.execute("""
            SELECT nombre FROM Productos 
            WHERE producto_id = %s AND usuario_id = %s
            """, (producto_id, session['user']['id']))
            producto = cur.fetchone()
            
            if not producto:
                flash('Producto no encontrado o no tienes permisos para eliminarlo', 'danger')
                return redirect(url_for('eliminar_producto'))
            
            # Eliminar el producto
            cur.execute("""
            DELETE FROM Productos 
            WHERE producto_id = %s AND usuario_id = %s
            """, (producto_id, session['user']['id']))
            conn.commit()
            
            flash(f'Producto "{producto[0]}" eliminado exitosamente!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error al eliminar producto: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()

    # Obtener lista de productos para mostrar
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT producto_id, nombre FROM Productos 
    WHERE usuario_id = %s ORDER BY producto_id DESC
    """, (session['user']['id'],))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('admin/eliminar_producto.html', productos=productos)

# Ruta para registrar venta
@app.route('/admin/registrar_venta', methods=['GET', 'POST'])
@login_required(role='vendedor')
def registrar_venta():
    if request.method == 'POST':
        # Procesar los productos vendidos
        productos_vendidos = []
        total = 0
        
        for key, value in request.form.items():
            if key.startswith('cantidad_'):
                producto_id = int(key.split('_')[1])
                cantidad = int(value)
                
                if cantidad > 0:
                    # Obtener detalles del producto
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""
                    SELECT producto_id, nombre, precio, stock 
                    FROM Productos 
                    WHERE producto_id = %s AND usuario_id = %s
                    """, (producto_id, session['user']['id']))
                    producto = cur.fetchone()
                    cur.close()
                    conn.close()
                    
                    if not producto:
                        flash(f'Producto ID {producto_id} no encontrado', 'danger')
                        return redirect(url_for('registrar_venta'))
                    
                    if cantidad > producto[3]:  # Verificar stock
                        flash(f'No hay suficiente stock para {producto[1]}. Disponible: {producto[3]}', 'danger')
                        return redirect(url_for('registrar_venta'))
                    
                    productos_vendidos.append({
                        'producto_id': producto[0],
                        'nombre': producto[1],
                        'precio': producto[2],
                        'cantidad': cantidad
                    })
                    total += producto[2] * cantidad
        
        if not productos_vendidos:
            flash('No se han seleccionado productos para vender', 'danger')
            return redirect(url_for('registrar_venta'))
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Registrar la venta
            cur.execute("""
            INSERT INTO Ventas (usuario_id, total) 
            VALUES (%s, %s) RETURNING venta_id
            """, (session['user']['id'], total))
            venta_id = cur.fetchone()[0]
            
            # Registrar detalles de venta y actualizar stock
            for producto in productos_vendidos:
                cur.execute("""
                INSERT INTO DetallesDeVenta (venta_id, producto_id, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
                """, (venta_id, producto['producto_id'], producto['cantidad'], producto['precio']))
                
                cur.execute("""
                UPDATE Productos 
                SET stock = stock - %s 
                WHERE producto_id = %s
                """, (producto['cantidad'], producto['producto_id']))
            
            conn.commit()
            flash(f'Venta registrada exitosamente! Total: ${total:.2f}', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error al registrar venta: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()

    # Obtener productos disponibles para vender
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT producto_id, nombre, precio, stock 
    FROM Productos 
    WHERE usuario_id = %s AND stock > 0
    ORDER BY nombre
    """, (session['user']['id'],))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('admin/registrar_venta.html', productos=productos)

# Ruta para generar reporte de productos
@app.route('/admin/generar_reporte_productos')
@login_required(role='vendedor')
def generar_reporte_productos():
    try:
        conn = get_db_connection()
        productos = pd.read_sql_query("""
        SELECT p.producto_id as ID, p.nombre as Nombre, p.descripcion as Descripción, 
               p.precio as Precio, p.stock as Stock, c.nombre as Categoría,
               p.fecha_de_caducidad as "Fecha de Caducidad", 
               p.codigo_de_barras as "Código de Barras",
               p.costo_de_compra as "Costo de Compra"
        FROM Productos p
        JOIN Categorias c ON p.categoria_id = c.categoria_id
        WHERE p.usuario_id = %s
        """, conn, params=(session['user']['id'],))
        
        if productos.empty:
            flash('No hay productos registrados para generar reporte', 'info')
            return redirect(url_for('admin_dashboard'))
        
        # Crear el reporte en memoria
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        productos.to_excel(writer, index=False, sheet_name='Productos')
        
        # Formatear el Excel
        workbook = writer.book
        worksheet = writer.sheets['Productos']
        
        # Ajustar el ancho de las columnas
        for i, col in enumerate(productos.columns):
            max_len = max((
                productos[col].astype(str).map(len).max(),  # Longitud máxima de los datos
                len(str(col))  # Longitud del nombre de la columna
            )) + 2  # Pequeño margen
            worksheet.set_column(i, i, max_len)
        
        writer.close()
        output.seek(0)
        
        # Enviar el archivo como descarga
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='reporte_productos.xlsx'
        )
    except Exception as e:
        flash(f'Error al generar reporte: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))
    finally:
        conn.close()

# Ruta para generar reporte de ventas
@app.route('/admin/generar_reporte_ventas')
@login_required(role='vendedor')
def generar_reporte_ventas():
    try:
        conn = get_db_connection()
        ventas = pd.read_sql_query("""
        SELECT 
            v.venta_id as "ID Venta",
            v.fecha as Fecha,
            p.nombre as Producto,
            dv.cantidad as Cantidad,
            dv.precio_unitario as "Precio Unitario",
            (dv.cantidad * dv.precio_unitario) as Total,
            p.codigo_de_barras as "Código de Barras"
        FROM Ventas v
        JOIN DetallesDeVenta dv ON v.venta_id = dv.venta_id
        JOIN Productos p ON dv.producto_id = p.producto_id
        WHERE v.usuario_id = %s
        ORDER BY v.fecha DESC
        """, conn, params=(session['user']['id'],))
        
        if ventas.empty:
            flash('No hay ventas registradas para generar reporte', 'info')
            return redirect(url_for('admin_dashboard'))
        
        # Crear el reporte en memoria
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        ventas.to_excel(writer, index=False, sheet_name='Ventas')
        
        # Formatear el Excel
        workbook = writer.book
        worksheet = writer.sheets['Ventas']
        
        # Ajustar el ancho de las columnas
        for i, col in enumerate(ventas.columns):
            max_len = max((
                ventas[col].astype(str).map(len).max(),  # Longitud máxima de los datos
                len(str(col))  # Longitud del nombre de la columna
            )) + 2  # Pequeño margen
            worksheet.set_column(i, i, max_len)
        
        writer.close()
        output.seek(0)
        
        # Enviar el archivo como descarga
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='reporte_ventas.xlsx'
        )
    except Exception as e:
        flash(f'Error al generar reporte: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))
    finally:
        conn.close()

# Ruta para predicción de demanda
@app.route('/admin/prediccion_demanda', methods=['GET', 'POST'])
@login_required(role='vendedor')
def prediccion_demanda():
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        
        try:
            conn = get_db_connection()
            
            # Obtener datos históricos de ventas
            df = pd.read_sql_query("""
            SELECT 
                v.fecha, 
                dv.cantidad 
            FROM Ventas v
            JOIN DetallesDeVenta dv ON v.venta_id = dv.venta_id
            WHERE dv.producto_id = %s AND v.usuario_id = %s
            ORDER BY v.fecha;
            """, conn, params=(producto_id, session['user']['id']))
            
            if df.empty:
                flash('No hay suficientes datos históricos para realizar la predicción', 'danger')
                return redirect(url_for('prediccion_demanda'))
            
            # Obtener nombre del producto
            cur = conn.cursor()
            cur.execute("SELECT nombre FROM Productos WHERE producto_id = %s", (producto_id,))
            nombre_producto = cur.fetchone()[0]
            cur.close()
            
            # Procesamiento de datos y predicción
            df['fecha'] = pd.to_datetime(df['fecha'])
            df['dias'] = (df['fecha'] - df['fecha'].min()).dt.days

            X = df[['dias']]
            y = df['cantidad']

            modelo = LinearRegression()
            modelo.fit(X, y)

            dias_futuros = pd.DataFrame({'dias': [df['dias'].max() + i for i in range(1, 31)]})
            predicciones = modelo.predict(dias_futuros)
            
            # Crear gráfico
            plt.figure(figsize=(10, 5))
            plt.plot(df['dias'], y, label="Histórico", marker='o')
            plt.plot(dias_futuros['dias'], predicciones, label="Predicción", linestyle="--")
            plt.xlabel("Días")
            plt.ylabel("Cantidad Vendida")
            plt.title(f"Predicción de Demanda: {nombre_producto}")
            plt.legend()
            
            # Guardar gráfico en memoria
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            # Convertir imagen a base64 para mostrar en HTML
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            
            # Preparar datos para la tabla de predicciones
            predicciones_dias = []
            for dia, pred in zip(dias_futuros['dias'], predicciones):
                predicciones_dias.append({
                    'dia': dia,
                    'prediccion': int(pred)
                })
            
            total_predicho = int(sum(predicciones))
            
            return render_template('admin/prediccion_demanda.html', 
                                nombre_producto=nombre_producto,
                                img_data=img_base64,
                                predicciones=predicciones_dias,
                                total_predicho=total_predicho,
                                mostrar_resultados=True)
            
        except Exception as e:
            flash(f'Error al realizar la predicción: {str(e)}', 'danger')
            return redirect(url_for('prediccion_demanda'))
        finally:
            conn.close()
    
    # Obtener lista de productos para el formulario
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.producto_id, p.nombre 
    FROM Productos p
    JOIN (
        SELECT producto_id 
        FROM DetallesDeVenta dv
        JOIN Ventas v ON dv.venta_id = v.venta_id
        WHERE v.usuario_id = %s
        GROUP BY producto_id
        HAVING COUNT(*) > 2
    ) AS vendidos ON p.producto_id = vendidos.producto_id
    WHERE p.usuario_id = %s
    """, (session['user']['id'], session['user']['id']))
    productos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('admin/prediccion_demanda.html', productos=productos, mostrar_resultados=False)

# ... (el resto del código se mantiene igual)
###############################
if __name__ == '__main__':
    app.run(debug=True)