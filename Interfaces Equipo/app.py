import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
from mysql.connector import connect, Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename 
from datetime import timedelta

## pip install Flask
## pip install mysql-connector-python
## pip install Werkzeug
## pip install Flask-WTF
## pip install WTForms
## pip install python-dotenv

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.secret_key = 'your_secret_key'

### imagenes
UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Función para verificar la extensión de los archivos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
### imagenes

# Conexión a la base de datos MySQL
def get_db_connection():
    return connect(
        host="localhost",
        user="root",
        password="",
        database="Gimnasio"
    )

# Página principal
@app.route('/')
def indexlogin():
    print("Accediendo a la ruta principal")
    return render_template('indexlogin.html')



@app.route('/index_cliente')
def index_cliente():
    if 'user_id' not in session:  # Verifica si el usuario está autenticado
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))
    
    user_id = session['user_id']  # ID del usuario de la sesión
    user_name = session.get('user_name')  # Recupera el nombre desde la sesión

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Obtener clases de la base de datos
        cursor.execute("SELECT * FROM clases")
        clases = cursor.fetchall()
        
        # Obtener membresías de la base de datos
        cursor.execute("SELECT * FROM membresias")
        membresias = cursor.fetchall()
        
        # Obtener los pagos del cliente y buscar el más caro
        cursor.execute("""
            SELECT p.ID_Pago, p.ID_Membresia, m.Tipo, p.Fecha_Pago, p.Monto, m.Duracion, m.Imagen, p.Metodo_Pago
            FROM pagos p
            JOIN membresias m ON p.ID_Membresia = m.ID_Membresia
            WHERE p.ID_Cliente = %s
        """, (user_id,))
        pagos = cursor.fetchall()

        # Inicializar la variable 'pago_mas_caro' para evitar el error si 'pagos' está vacío
        pago_mas_caro = None

        # Encontrar el pago más caro si existen pagos
        if pagos:
            pago_mas_caro = max(pagos, key=lambda x: x['Monto'])  # Pago con el monto más alto
            
            # Calcular la fecha de inicio y fin
            fecha_pago = pago_mas_caro['Fecha_Pago']
            duracion = pago_mas_caro['Duracion']
            fecha_inicio = fecha_pago
            fecha_fin = (fecha_pago + timedelta(days=duracion))  # Fecha final sumando la duración
            
            # Agregar estos datos al pago más caro
            pago_mas_caro['Fecha_Inicio'] = fecha_inicio
            pago_mas_caro['Fecha_Fin'] = fecha_fin

    finally:
        cursor.close()
        db.close()

    # Pasar las clases, membresías, pagos y la membresía más cara al renderizar la plantilla
    return render_template('indexclientes.html', user_name=user_name, clases=clases, membresias=membresias, pagos=pagos, pago_mas_caro=pago_mas_caro)

    
@app.route('/index_admin')
def index_admin():
    if 'admin_id' in session:
        return render_template('indexadmin.html')
    else:
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    telefono = request.form.get('telefono')  # Opcional
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    direccion = request.form.get('direccion')  # Opcional
    imagen = None  # Inicializa la variable para la imagen

    # Directorio de carga para las imágenes de clientes
    UPLOAD_FOLDER = 'src/static/clientes'

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):  # Valida el archivo
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))  # Guarda el archivo
            imagen = f'clientes/{filename}'  # Ruta relativa para guardar en la base de datos

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO clientes (Nombre, Apellido, Fecha_Nacimiento, Telefono, Email, Password, Direccion, Imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, fecha_nacimiento, telefono, email, password, direccion, imagen))
        db.commit()
        flash("Registro exitoso.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('indexlogin'))



@app.route('/logout')
def logout():
    session.clear()  # Elimina la información del usuario de la sesión
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('indexlogin'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes WHERE Email=%s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['ID_Cliente']
            session['user_name'] = user['Nombre']  # Guarda el nombre del cliente
            session['user_image'] = user['Imagen']  # Guarda la imagen del cliente
            flash("Inicio de sesión exitoso.")
            return redirect(url_for('index_cliente'))
        else:
            flash("Credenciales incorrectas.")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('indexlogin'))


@app.route('/admin/login', methods=['POST'])
def admin_login():
    user = request.form['user']
    password = request.form['password']

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Administradores WHERE User=%s", (user,))
        admin = cursor.fetchone()
        if admin and check_password_hash(admin['Password'], password):
            session['admin_id'] = admin['ID_Admin']
            flash("Inicio de sesión exitoso como administrador.")
            return redirect(url_for('index_admin'))  # Redirige a la vista del administrador
        else:
            flash("Credenciales incorrectas.")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('indexlogin'))

@app.route('/some_protected_route')
def some_protected_route():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para acceder.")
        return redirect(url_for('indexlogin'))
    # Lógica para la vista protegida


@app.route('/guardar_clase', methods=['POST'])
def guardar_clase():
    if 'imagen' not in request.files:
        flash('No se ha seleccionado una imagen')
        return redirect(request.url)
    
    imagen = request.files['imagen']
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        imagen_path = None
    
    # Guardar la clase en la base de datos, incluyendo la ruta de la imagen
    nombre_clase = request.form['nombre_clase']
    descripcion = request.form['descripcion']
    instructor = request.form['instructor']
    hora = request.form['hora']
    capacidad = request.form['capacidad']
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO clases (Nombre_Clase, Descripcion, Instructor, Hora, Capacidad, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_clase, descripcion, instructor, hora, capacidad, imagen_path))
        db.commit()
        flash("Clase guardada exitosamente.")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('index_cliente'))

# CRUD para la tabla Clientes
@app.route('/clientes')
def clientes():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        return render_template('clientes.html', clientes=clientes)
    finally:
        cursor.close()
        db.close()

@app.route('/clientes/add', methods=['POST'])
def add_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    telefono = request.form['telefono']
    email = request.form['email']
    direccion = request.form['direccion']
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Clientes (Nombre, Apellido, Fecha_Nacimiento, Telefono, Email, Direccion) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (nombre, apellido, fecha_nacimiento, telefono, email, direccion))
        db.commit()
        flash("Cliente agregado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('clientes'))

# Ruta para actualizar un pago
@app.route('/pagos/update/<int:id>', methods=['POST'])
def update_pago(id):
    id_cliente = request.form['id_cliente']
    id_membresia = request.form['id_membresia']
    monto = request.form['monto']
    metodo_pago = request.form['metodo_pago']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""UPDATE Pagos SET ID_Cliente=%s, ID_Membresia=%s, Monto=%s, Metodo_Pago=%s 
                      WHERE ID_Pago=%s""",
                   (id_cliente, id_membresia, monto, metodo_pago, id))
    db.commit()
    cursor.close()
    db.close()
    flash("Pago actualizado exitosamente.")
    return redirect(url_for('pagos'))

@app.route('/personal/update/<int:id>', methods=['POST'])
def update_personal(id):
    nombre = request.form['nombre']
    puesto = request.form['puesto']
    salario = request.form['salario']
    antiguedad = request.form['antiguedad']
    turno = request.form['turno']
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""UPDATE Personal SET Nombre=%s, Puesto=%s, Salario=%s, Antiguedad=%s, Turno=%s 
                          WHERE ID_Personal=%s""",
                       (nombre, puesto, salario, antiguedad, turno, id))
        db.commit()
        flash("Personal actualizado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('personal'))

@app.route('/membresias/update/<int:id>', methods=['POST'])
def update_membresia(id):
    tipo = request.form['tipo']
    costo = request.form['costo']
    duracion = request.form['duracion']
    descripcion = request.form['descripcion']
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""UPDATE Membresias SET Tipo=%s, Costo=%s, Duracion=%s, Descripcion=%s 
                          WHERE ID_Membresia=%s""",
                       (tipo, costo, duracion, descripcion, id))
        db.commit()
        flash("Membresía actualizada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('membresias'))

@app.route('/clases/edit/<int:id>', methods=['POST'])
def edit_clase(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    instructor = request.form['instructor']
    hora = request.form['hora']
    capacidad = request.form['capacidad']
    imagen = None

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            imagen = f'uploads/{filename}'

    try:
        db = get_db_connection()
        cursor = db.cursor()
        if imagen:
            cursor.execute("""
                UPDATE Clases 
                SET Nombre_Clase = %s, Descripcion = %s, Instructor = %s, Hora = %s, Capacidad = %s, Imagen = %s 
                WHERE ID_Clase = %s""",
                (nombre, descripcion, instructor, hora, capacidad, imagen, id))
        else:
            cursor.execute("""
                UPDATE Clases 
                SET Nombre_Clase = %s, Descripcion = %s, Instructor = %s, Hora = %s, Capacidad = %s 
                WHERE ID_Clase = %s""",
                (nombre, descripcion, instructor, hora, capacidad, id))
        db.commit()
        flash("Clase editada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('clases'))


@app.route('/historial_pagos')
def historial_pagos():
    if 'user_id' not in session:  # Verifica si el usuario está autenticado
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))
    
    user_id = session['user_id']  # ID del usuario de la sesión

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Obtener los pagos del cliente
        cursor.execute("""
            SELECT p.ID_Pago, m.Tipo, p.Fecha_Pago, p.Monto, p.Metodo_Pago
            FROM pagos p
            JOIN membresias m ON p.ID_Membresia = m.ID_Membresia
            WHERE p.ID_Cliente = %s
        """, (user_id,))
        pagos = cursor.fetchall()

    finally:
        cursor.close()
        db.close()

    return render_template('indexclientes.html', pagos=pagos)  # Asegúrate de pasar los pagos al renderizar la plantilla


@app.route('/clientes/edit/<int:id>', methods=['POST'])
def edit_cliente(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']  # Agregar la fecha de nacimiento
    telefono = request.form['telefono']
    email = request.form['email']
    direccion = request.form['direccion']
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE Clientes 
            SET Nombre = %s, Apellido = %s, Fecha_Nacimiento = %s, Telefono = %s, Email = %s, Direccion = %s 
            WHERE ID_Cliente = %s""",
            (nombre, apellido, fecha_nacimiento, telefono, email, direccion, id))  # Asegúrate de incluir fecha_nacimiento
        db.commit()
        flash("Cliente editado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('clientes'))

@app.route('/pagar_membresia', methods=['POST'])
def pagar_membresia():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))
    
    id_cliente = session['user_id']
    id_membresia = request.form['id_membresia']
    metodo_pago = request.form['metodo_pago']

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Obtener el costo de la membresía
        cursor.execute("SELECT Costo FROM membresias WHERE ID_Membresia = %s", (id_membresia,))
        membresia = cursor.fetchone()
        if not membresia:
            flash("La membresía seleccionada no existe.")
            return redirect(url_for('index_cliente'))
        
        monto = membresia['Costo']

        # Registrar el pago
        cursor.execute("""
            INSERT INTO pagos (ID_Cliente, ID_Membresia, Monto, Metodo_Pago) 
            VALUES (%s, %s, %s, %s)
        """, (id_cliente, id_membresia, monto, metodo_pago))
        db.commit()
        flash("Pago realizado con éxito.")
    except Exception as e:
        flash(f"Error al registrar el pago: {e}")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('index_cliente'))


@app.route('/clientes/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Verifica si el cliente existe antes de intentar eliminarlo
        cursor.execute("SELECT * FROM Clientes WHERE ID_Cliente = %s", (id,))
        cliente = cursor.fetchone()

        if not cliente:
            flash("El cliente no existe o ya fue eliminado.")
            return redirect(url_for('clientes'))

        # Intenta eliminar el cliente
        cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = %s", (id,))
        db.commit()
        flash("Cliente eliminado exitosamente.")
    except Error as e:
        flash(f"Error al eliminar el cliente: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('clientes'))



@app.route('/get_clases')
def get_clases():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clases")
        clases = cursor.fetchall()
    finally:
        cursor.close()
        db.close()
    return render_template('indexclientes.html', clases=clases)
    



@app.route('/clases/delete/<int:id>', methods=['POST'])
def delete_clase(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Clases WHERE ID_Clase = %s", (id,))
        db.commit()
        flash("Clase eliminada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('clases'))



# CRUD para la tabla Clases
@app.route('/clases')
def clases():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clases")
        clases = cursor.fetchall()
        return render_template('clases.html', clases=clases)
    finally:
        cursor.close()
        db.close()

@app.route('/clases/add', methods=['POST'])
def add_clase():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    instructor = request.form['instructor']
    hora = request.form['hora']
    capacidad = request.form['capacidad']
    imagen = None

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            imagen = f'uploads/{filename}'

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Clases (Nombre_Clase, Descripcion, Instructor, Hora, Capacidad, Imagen) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (nombre, descripcion, instructor, hora, capacidad, imagen))
        db.commit()
        flash("Clase agregada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('clases'))



# CRUD para la tabla Membresías
@app.route('/membresias')
def membresias():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Membresias")
        membresias = cursor.fetchall()
        return render_template('membresias.html', membresias=membresias)
    finally:
        cursor.close()
        db.close()

@app.route('/membresias/add', methods=['POST'])
def add_membresia():
    tipo = request.form['tipo']
    costo = request.form['costo']
    duracion = request.form['duracion']
    descripcion = request.form['descripcion']
    imagen = None

    # Verificar si se subió una imagen
    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            # Asegurarse de que el nombre del archivo sea seguro
            filename = secure_filename(file.filename)
            # Guardar la imagen en el directorio adecuado
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            imagen = f'uploads/{filename}'  # Ruta para guardar en la base de datos

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Membresias (Tipo, Costo, Duracion, Descripcion, Imagen) 
            VALUES (%s, %s, %s, %s, %s)""",
            (tipo, costo, duracion, descripcion, imagen))
        db.commit()
        flash("Membresía agregada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('membresias'))

@app.route('/membresias/delete/<int:id>', methods=['POST'])
def delete_membresia(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Membresias WHERE ID_Membresia=%s", (id,))
        db.commit()
        flash("Membresía eliminada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('membresias'))


# Ruta para ver todos los pagos
@app.route('/pagos')
def pagos():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Pagos")
    pagos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('pagos.html', pagos=pagos)


# Ruta para agregar un pago
@app.route('/pagos/add', methods=['POST'])
def add_pago():
    id_cliente = request.form['id_cliente']
    id_membresia = request.form['id_membresia']
    monto = request.form['monto']
    metodo_pago = request.form['metodo_pago']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Pagos (ID_Cliente, ID_Membresia, Monto, Metodo_Pago) VALUES (%s, %s, %s, %s)",
                   (id_cliente, id_membresia, monto, metodo_pago))
    db.commit()
    cursor.close()
    db.close()
    flash("Pago agregado exitosamente.")
    return redirect(url_for('pagos'))

# Ruta para eliminar un pago
@app.route('/pagos/delete/<int:id>', methods=['POST'])
def delete_pago(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Pagos WHERE ID_Pago=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    flash("Pago eliminado exitosamente.")
    return redirect(url_for('pagos'))  # Retornando una respuesta válida

# CRUD para la tabla Personal
@app.route('/personal')
def personal():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Personal")
        personal = cursor.fetchall()
        return render_template('personal.html', personal=personal)
    finally:
        cursor.close()
        db.close()

@app.route('/personal/add', methods=['POST'])
def add_personal():
    nombre = request.form['nombre']
    puesto = request.form['puesto']
    salario = request.form['salario']
    antiguedad = request.form['antiguedad']
    turno = request.form['turno']
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Personal (Nombre, Puesto, Salario, Antiguedad, Turno) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, puesto, salario, antiguedad, turno))
        db.commit()
        flash("Personal agregado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('personal'))

@app.route('/personal/delete/<int:id>', methods=['GET'])
def delete_personal(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Personal WHERE ID_Personal=%s", (id,))
        db.commit()
        flash("Personal eliminado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('personal'))

if __name__ == '__main__':
    app.run(debug=True)
