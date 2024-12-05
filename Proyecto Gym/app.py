import os
from flask import Flask, render_template, request, redirect, flash, url_for, session, send_file
from mysql.connector import connect, Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename 
from datetime import timedelta
from fpdf import FPDF
from uuid import uuid4
import hashlib
import random
import string

## pip install Flask
## pip install mysql-connector-python
# En caso de inconvenientes 
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

def index():
    print("Accediendo a la ruta principal")
    return render_template('index.html')
@app.route('/indexlogin')
def indexlogin():
    print("Accediendo a la ruta principal")
    return render_template('indexlogin.html')
@app.route('/services')
def services():
    return render_template('info.html')

@app.route('/schedules')
def schedules():
    return render_template('membresia.html')

@app.route('/trainers')
def trainers():
    return render_template('sobre_nosotros.html')

@app.route('/pricing')
def pricing():
    return render_template('class.html')

@app.route('/location')
def location():
    return render_template('perron.html')

#Pagina para inicio de sesión de administradores
@app.route('/AdminLogin')
def admin_login_template():
    return render_template('adminlogin.html')


## FUNCIONES DE SESIÓN ##
# Función para obtener la conexión a la base de datos
def get_cursor():
    db = get_db_connection()
    return db, db.cursor(dictionary=True)

# Función para obtener todas las membresías disponibles
def obtener_membresias():
    db, cursor = get_cursor()
    try:
        cursor.execute("SELECT * FROM membresias")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

# Función para obtener la membresía activa del cliente
def obtener_membresia_activa(user_id):
    db, cursor = get_cursor()
    try:
        cursor.execute("""
        SELECT p.ID_Membresia, m.Tipo, m.Descripcion, m.Duracion, p.Monto, m.Imagen
        FROM pagos p
        JOIN membresias m ON p.ID_Membresia = m.ID_Membresia
        WHERE p.ID_Cliente = %s AND p.Estado_Membresia = 'Activo'
        ORDER BY p.Fecha_Pago DESC LIMIT 1
        """, (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        db.close()

# Función para obtener las clases asociadas a una membresía activa
def obtener_clases_membresia(id_membresia):
    db, cursor = get_cursor()
    try:
        cursor.execute("""
        SELECT 
            c.*,
            p.Nombre AS Instructor,
            (SELECT COUNT(*) FROM Inscripciones WHERE ID_Clase = c.ID_Clase) AS Inscritos
        FROM Clases c
        JOIN membresias_clases mc ON c.ID_Clase = mc.ID_Clase
        LEFT JOIN Personal p ON c.ID_Personal = p.ID_Personal
        WHERE mc.ID_Membresia = %s
        """, (id_membresia,))
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


# Función para obtener el historial de pagos de un cliente
def obtener_pagos_cliente(user_id):
    db, cursor = get_cursor()
    try:
        cursor.execute("""
        SELECT p.ID_Pago, p.ID_Membresia, m.Tipo, p.Fecha_Pago, p.Monto, m.Duracion, m.Imagen, p.Metodo_Pago, p.Estado, p.Estado_Membresia, p.Referencia
        FROM pagos p
        JOIN membresias m ON p.ID_Membresia = m.ID_Membresia
        WHERE p.ID_Cliente = %s
        """, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

@app.route('/registrarse_clase/<int:id_clase>', methods=['POST'])
def registrarse_clase(id_clase):
    if 'user_id' not in session:  # Verifica si el usuario está autenticado
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))

    user_id = session['user_id']
    
    db, cursor = get_cursor()
    try:
        # Verificar si el cliente ya está inscrito en la clase
        cursor.execute("SELECT COUNT(*) AS count FROM Inscripciones WHERE ID_Cliente = %s AND ID_Clase = %s", (user_id, id_clase))
        inscrito = cursor.fetchone()['count'] > 0

        if inscrito:
            flash("Ya estás registrado en esta clase.", "info")
            return redirect(url_for('index_cliente'))

        # Verificar capacidad de la clase
        cursor.execute("SELECT Capacidad, (SELECT COUNT(*) FROM Inscripciones WHERE ID_Clase = %s) AS Inscritos FROM Clases WHERE ID_Clase = %s", (id_clase, id_clase))
        clase = cursor.fetchone()

        if clase and clase['Inscritos'] < clase['Capacidad']:
            # Registrar inscripción
            cursor.execute("INSERT INTO Inscripciones (ID_Clase, ID_Cliente) VALUES (%s, %s)", (id_clase, user_id))
            db.commit()
            flash("Te has registrado exitosamente en la clase.", "success")
        else:
            flash("Esta clase está llena. No es posible registrarte.", "danger")
    except Exception as e:
        db.rollback()
        flash("Ocurrió un error al intentar registrarte: " + str(e), "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('index_cliente'))

@app.route('/salir_clase/<int:id_clase>', methods=['POST'])
def salir_clase(id_clase):
    if 'user_id' not in session:  # Verifica si el usuario está autenticado
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))

    user_id = session['user_id']

    db, cursor = get_cursor()
    try:
        # Eliminar inscripción de la tabla Inscripciones
        cursor.execute("DELETE FROM Inscripciones WHERE ID_Cliente = %s AND ID_Clase = %s", (user_id, id_clase))
        db.commit()
        flash("Has salido de la clase exitosamente.", "success")
    except Exception as e:
        db.rollback()
        flash("Ocurrió un error al intentar salir de la clase: " + str(e), "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('index_cliente'))


def verificar_inscripcion(id_cliente, id_clase):
    db, cursor = get_cursor()
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM Inscripciones WHERE ID_Cliente = %s AND ID_Clase = %s", (id_cliente, id_clase))
        return cursor.fetchone()['count'] > 0
    finally:
        cursor.close()
        db.close()


# Ruta principal del cliente 
@app.route('/index_cliente')
def index_cliente():
    if 'user_id' not in session:  # Verifica si el usuario está autenticado
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('indexlogin'))
    
    user_id = session['user_id']
    user_name = session.get('user_name')
    
    # Llamar funciones segmentadas
    membresias = obtener_membresias()
    membresia_activa = obtener_membresia_activa(user_id)
    clases = []
    if membresia_activa:
        clases = obtener_clases_membresia(membresia_activa['ID_Membresia'])
        for clase in clases:
            # Verificar si el cliente está inscrito en cada clase
            clase['Inscrito'] = verificar_inscripcion(user_id, clase['ID_Clase'])
    pagos = obtener_pagos_cliente(user_id)

    # Renderizar plantilla con datos obtenidos
    return render_template(
        'indexclientes.html', 
        user_name=user_name, 
        clases=clases, 
        membresias=membresias, 
        pagos=pagos, 
        membresia_activa=membresia_activa
    )
    
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
    password = request.form['password']  # No se genera un hash, se guarda la contraseña tal cual
    direccion = request.form.get('direccion')  # Opcional
    imagen = None  # Inicializa la variable para la imagen

    # Directorio de carga para las imágenes de clientes
    UPLOAD_FOLDER = 'src/static/clientes'

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):  # Valida el archivo
            # Generar un nombre único para la imagen
            unique_filename = f"{uuid4().hex}{os.path.splitext(file.filename)[1]}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)  # Guarda el archivo
            imagen = f'clientes/{unique_filename}'  # Ruta relativa para guardar en la base de datos

    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Verifica si el correo ya está registrado
        cursor.execute("SELECT * FROM Clientes WHERE Email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("ERROR! Correo ya registrado, intenta con otro diferente.", "error")
            return redirect(url_for('indexlogin'))  # Redirige al formulario de registro

        # Inserta el nuevo cliente si el correo no está registrado
        cursor.execute("""
            INSERT INTO Clientes (Nombre, Apellido, Fecha_Nacimiento, Telefono, Email, Password, Direccion, Imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, fecha_nacimiento, telefono, email, password, direccion, imagen))
        db.commit()
        flash("Registro exitoso.", "success")
    except Error as e:
        flash(f"Error: {e}", "error")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('indexlogin'))


@app.route('/logout')
def logout():
    session.clear()  # Elimina la información del usuario de la sesión
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('indexlogin'))

@app.route('/logoutadmin')
def logoutadmin():
    session.clear()  # Elimina la información del usuario del admin 
    flash("Sesión de administrador cerrada correctamente")
    return redirect(url_for('admin_login_template'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes WHERE Email=%s", (email,))
        user = cursor.fetchone()
        if user and user['password'] == password:  # Compara directamente la contraseña (sin hash)
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


# Ruta para el inicio de sesión de administradores
@app.route('/admin/login', methods=['POST'])
def admin_login():
    # Obtiene el usuario y la contraseña desde el formulario enviado
    user = request.form['user']
    password = request.form['password']

    try:
        # Establece la conexión con la base de datos
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)  # Usa un cursor que devuelve filas como diccionarios

        # Consulta para buscar al administrador por su nombre de usuario
        cursor.execute("SELECT * FROM Administradores WHERE User=%s", (user,))
        admin = cursor.fetchone()  # Obtiene la primera fila del resultado

        # Si se encuentra un administrador y la contraseña es válida
        if admin and check_password_hash(admin['Password'], password):
            # Guarda el ID del administrador en la sesión para mantener la autenticación
            session['admin_id'] = admin['ID_Admin']

            # Muestra un mensaje de éxito al administrador
            flash("Inicio de sesión exitoso como administrador.")

            # Redirige al administrador a su panel principal
            return redirect(url_for('index_admin'))
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            flash("Credenciales incorrectas.")
    finally:
        # Cierra el cursor y la conexión a la base de datos para liberar recursos
        cursor.close()
        db.close()

    # Si la autenticación falla, redirige al formulario de inicio de sesión de administradores
    return redirect(url_for('admin_login_template'))

@app.route('/some_protected_route')
def some_protected_route():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para acceder.")
        return redirect(url_for('indexlogin'))
    # Lógica para la vista protegida


@app.route('/guardar_clase', methods=['POST'])
def guardar_clase():
    UPLOAD_FOLDER = '/home/FerAzuI/gimnasio/src/static/uploads'
    imagen_path = None

    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen and allowed_file(imagen.filename):
            # Generar un nombre único para la imagen
            unique_filename = f"{uuid4().hex}{os.path.splitext(imagen.filename)[1]}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            imagen.save(file_path)
            imagen_path = f'uploads/{unique_filename}'  # Ruta relativa para la base de datos

    # Guardar la clase en la base de datos
    nombre_clase = request.form['nombre_clase']
    descripcion = request.form['descripcion']
    instructor_id = request.form['instructor_id']
    hora = request.form['hora']
    capacidad = request.form['capacidad']

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO clases (Nombre_Clase, Descripcion, ID_Personal, Hora, Capacidad, Imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_clase, descripcion, instructor_id, hora, capacidad, imagen_path))
        db.commit()
        flash("Clase guardada exitosamente.", "success")
    except Error as e:
        flash(f"Error: {e}", "error")
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

@app.route('/pagos/update/<int:id>', methods=['POST'])
def update_pago(id):
    # Recuperar datos del formulario
    id_cliente = request.form['id_cliente']
    id_membresia = request.form['id_membresia']
    monto = request.form['monto']
    metodo_pago = request.form['metodo_pago']
    estado = request.form['estado']
    referencia = request.form['referencia']
    estado_membresia = request.form['estado_membresia']

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Validar existencia de ID_Cliente
    cursor.execute("SELECT COUNT(*) AS count FROM Clientes WHERE ID_Cliente = %s", (id_cliente,))
    if cursor.fetchone()['count'] == 0:
        flash("El cliente seleccionado no existe.", "danger")
        return redirect(url_for('pagos'))

    # Validar existencia de ID_Membresia
    cursor.execute("SELECT COUNT(*) AS count FROM Membresias WHERE ID_Membresia = %s", (id_membresia,))
    if cursor.fetchone()['count'] == 0:
        flash("La membresía seleccionada no existe.", "danger")
        return redirect(url_for('pagos'))

    # Ejecutar la actualización
    cursor.execute("""
        UPDATE Pagos
        SET ID_Cliente=%s, ID_Membresia=%s, Monto=%s, Metodo_Pago=%s, Estado=%s, Referencia=%s, Estado_Membresia=%s 
        WHERE ID_Pago=%s
    """, (id_cliente, id_membresia, monto, metodo_pago, estado, referencia, estado_membresia, id))
    db.commit()

    cursor.close()
    db.close()

    flash("Pago actualizado exitosamente.", "success")
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
    id_instructor = request.form['instructor']
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
                SET Nombre_Clase = %s, Descripcion = %s, ID_Personal = %s, Hora = %s, Capacidad = %s, Imagen = %s 
                WHERE ID_Clase = %s""",
                (nombre, descripcion, id_instructor, hora, capacidad, imagen, id))
        else:
            cursor.execute("""
                UPDATE Clases 
                SET Nombre_Clase = %s, Descripcion = %s, ID_Personal = %s, Hora = %s, Capacidad = %s 
                WHERE ID_Clase = %s""",
                (nombre, descripcion, id_instructor, hora, capacidad, id))
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
        cursor.execute("SELECT Costo FROM Membresias WHERE ID_Membresia = %s", (id_membresia,))
        membresia = cursor.fetchone()
        if not membresia:
            flash("La membresía seleccionada no existe.")
            return redirect(url_for('index_cliente'))
        
        monto = membresia['Costo']

        # Generar una referencia única y encriptada
        raw_reference = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        referencia = hashlib.sha256(raw_reference.encode()).hexdigest()[:10]

        # Registrar el pago con estado "Pendiente" y estado de membresía "Inactivo"
        cursor.execute("""
            INSERT INTO Pagos (ID_Cliente, ID_Membresia, Fecha_Pago, Monto, Metodo_Pago, Estado, Referencia, Estado_Membresia) 
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s)
        """, (id_cliente, id_membresia, monto, metodo_pago, 'Pendiente', referencia, 'Inactivo'))
        db.commit()

        # Generar PDF de recibo
        pdf_path = generar_recibo_pdf(id_cliente, id_membresia, monto, metodo_pago, referencia)

        # Descargar automáticamente el PDF
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        flash(f"Error al registrar el pago: {e}")
        return redirect(url_for('index_cliente'))
    finally:
        cursor.close()
        db.close()


def generar_recibo_pdf(id_cliente, id_membresia, monto, metodo_pago, referencia):
    # Crear el objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del recibo
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Recibo de Pago", ln=True, align='C')
    pdf.ln(10)  # Espacio entre líneas

    # Información del cliente y pago
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID Cliente: {id_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"ID Membresía: {id_membresia}", ln=True)
    pdf.cell(200, 10, txt=f"Método de Pago: {metodo_pago}", ln=True)
    pdf.cell(200, 10, txt=f"Monto: ${monto:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Referencia: {referencia}", ln=True)
    pdf.cell(200, 10, txt="Estado: Pendiente", ln=True)
    pdf.cell(200, 10, txt="Transferencia Bancaria: 8901 3801 0238 0012", ln=True)
    pdf.cell(200, 10, txt="Deposito en efectivo: 09128390103020012023", ln=True)
    # Pie de página
    pdf.ln(20)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Gracias por su pago. Este es un recibo provisional.", ln=True, align='C')

    # Guardar PDF en un archivo temporal
    pdf_path = f"src/static/recibos/recibo_{id_cliente}_{referencia}.pdf"
    pdf.output(pdf_path)
    return pdf_path

@app.route('/descargar_recibo/<int:id_cliente>/<string:referencia>')
def descargar_recibo(id_cliente, referencia):
    # Obtener detalles del pago desde la base de datos
    db, cursor = get_cursor()
    try:
        cursor.execute("""
        SELECT p.ID_Membresia, p.Monto, p.Metodo_Pago, p.Referencia
        FROM Pagos p
        WHERE p.Referencia = %s AND p.ID_Cliente = %s
        """, (referencia, id_cliente))
        pago = cursor.fetchone()

        if not pago:
            flash("No se encontró el recibo solicitado.", "danger")
            return redirect(url_for('index_cliente'))

        # Generar el recibo PDF
        pdf_path = generar_recibo_pdf(
            id_cliente=id_cliente,
            id_membresia=pago['ID_Membresia'],
            monto=pago['Monto'],
            metodo_pago=pago['Metodo_Pago'],
            referencia=pago['Referencia']
        )
    finally:
        cursor.close()
        db.close()

    # Enviar el archivo PDF al cliente
    return send_file(pdf_path, as_attachment=True, download_name=f"recibo_{referencia}.pdf")


@app.route('/clientes/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Verifica si el cliente existe y obtiene la ruta de la imagen
        cursor.execute("SELECT Imagen FROM Clientes WHERE ID_Cliente = %s", (id,))
        cliente = cursor.fetchone()

        if not cliente:
            flash("El cliente no existe o ya fue eliminado.", "warning")
            return redirect(url_for('clientes'))

        # Eliminar la imagen del sistema de archivos si existe
        imagen = cliente[0]  # Accede al primer (y único) elemento de la tupla
        if imagen:
            image_path = os.path.join('src/static', imagen)  # Asegúrate de usar la ruta relativa correcta
            if os.path.exists(image_path):
                os.remove(image_path)

        # Eliminar el cliente de la base de datos
        cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = %s", (id,))
        db.commit()
        flash("Cliente eliminado exitosamente.", "success")
    except Error as e:
        flash(f"Error al eliminar el cliente: {e}", "error")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('clientes'))


@app.route('/clases/delete/<int:id>', methods=['POST'])
def delete_clase(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Recuperar la ruta de la imagen de la clase
        cursor.execute("SELECT Imagen FROM Clases WHERE ID_Clase = %s", (id,))
        clase = cursor.fetchone()

        if not clase:
            flash("La clase no existe o ya fue eliminada.", "warning")
            return redirect(url_for('clases'))

        # Eliminar la imagen si existe
        imagen = clase[0]  # Acceder al primer (y único) elemento de la tupla
        if imagen:
            image_path = os.path.join('src/static', imagen)
            if os.path.exists(image_path):
                os.remove(image_path)

        # Eliminar la clase de la base de datos
        cursor.execute("DELETE FROM Clases WHERE ID_Clase = %s", (id,))
        db.commit()
        flash("Clase eliminada exitosamente.", "success")
    except Error as e:
        flash(f"Error al eliminar la clase: {e}", "error")
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
        # Obtener clases con los nombres de los entrenadores
        query = """
        SELECT c.ID_Clase, c.Nombre_Clase, c.Descripcion, p.Nombre AS Instructor, c.Hora, c.Capacidad, c.Imagen
        FROM Clases c
        LEFT JOIN Personal p ON c.ID_Personal = p.ID_Personal
        WHERE p.Puesto = 'Entrenador' OR c.ID_Personal IS NULL;
        """
        cursor.execute(query)
        clases = cursor.fetchall()
        # Obtener entrenadores para el formulario
        cursor.execute("SELECT ID_Personal, Nombre FROM Personal WHERE Puesto = 'Entrenador';")
        entrenadores = cursor.fetchall()
        return render_template('clases.html', clases=clases, entrenadores=entrenadores)
    finally:
        cursor.close()
        db.close()


@app.route('/clases/add', methods=['POST'])
def add_clase():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    id_instructor = request.form['instructor']
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
            INSERT INTO Clases (Nombre_Clase, Descripcion, ID_Personal, Hora, Capacidad, Imagen) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (nombre, descripcion, id_instructor, hora, capacidad, imagen))
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
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Obtener membresías
    cursor.execute("SELECT * FROM Membresias")
    membresias = cursor.fetchall()

    # Agregar clases asociadas a cada membresía
    # Agregar clases asociadas a cada membresía
    for membresia in membresias:
        cursor.execute("""
            SELECT C.ID_Clase, C.Nombre_Clase 
            FROM Clases C 
            INNER JOIN Membresias_Clases MC 
            ON C.ID_Clase = MC.ID_Clase
            WHERE MC.ID_Membresia = %s
        """, (membresia['ID_Membresia'],))
        # Cambia para almacenar un diccionario con 'ID_Clase' y 'Nombre_Clase'
        clases_asociadas = cursor.fetchall()
        membresia['Clases'] = clases_asociadas

    # Obtener clases disponibles para el dropdown
    cursor.execute("SELECT ID_Clase, Nombre_Clase FROM Clases")
    clases_disponibles = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('membresias.html', membresias=membresias, clases_disponibles=clases_disponibles)



@app.route('/membresias/<int:membresia_id>/add_clase', methods=['POST'])
def add_clase_to_membresia(membresia_id):
    clase_id = request.form['clase_id']
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO Membresias_Clases (ID_Membresia, ID_Clase) 
            VALUES (%s, %s)
        """, (membresia_id, clase_id))
        db.commit()
        flash("Clase agregada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('membresias'))

@app.route('/membresias/<int:membresia_id>/delete_clase/<int:clase_id>', methods=['POST'])
def delete_clase_from_membresia(membresia_id, clase_id):
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            DELETE FROM Membresias_Clases 
            WHERE ID_Membresia = %s AND ID_Clase = %s
        """, (membresia_id, clase_id))
        db.commit()
        flash("Clase eliminada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('membresias'))

@app.route('/membresias/add', methods=['POST'])
def add_membresia():
    UPLOAD_FOLDER = '/home/FerAzuI/gimnasio/src/static/uploads'
    imagen = None

    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            unique_filename = f"{uuid4().hex}{os.path.splitext(file.filename)[1]}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            imagen = f'uploads/{unique_filename}'  # Ruta para guardar en la base de datos

    tipo = request.form['tipo']
    costo = request.form['costo']
    duracion = request.form['duracion']
    descripcion = request.form['descripcion']

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Membresias (Tipo, Costo, Duracion, Descripcion, Imagen) 
            VALUES (%s, %s, %s, %s, %s)
        """, (tipo, costo, duracion, descripcion, imagen))
        db.commit()
        flash("Membresía agregada exitosamente.", "success")
    except Error as e:
        flash(f"Error: {e}", "error")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('membresias'))

@app.route('/membresias/delete/<int:id>', methods=['POST'])
def delete_membresia(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Recuperar la ruta de la imagen de la membresía
        cursor.execute("SELECT Imagen FROM Membresias WHERE ID_Membresia = %s", (id,))
        membresia = cursor.fetchone()

        if not membresia:
            flash("La membresía no existe o ya fue eliminada.", "warning")
            return redirect(url_for('membresias'))

        # Eliminar la imagen si existe
        imagen = membresia[0]  # Accede al primer (y único) elemento de la tupla
        if imagen:
            image_path = os.path.join('src/static', imagen)
            if os.path.exists(image_path):
                os.remove(image_path)

        # Eliminar la membresía de la base de datos
        cursor.execute("DELETE FROM Membresias WHERE ID_Membresia = %s", (id,))
        db.commit()
        flash("Membresía eliminada exitosamente.", "success")
    except Error as e:
        flash(f"Error al eliminar la membresía: {e}", "error")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('membresias'))

# Ruta para ver todos los pagos
@app.route('/pagos', methods=['GET'])
def pagos():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Recuperar el término de búsqueda de la solicitud
    query_param = request.args.get('query', '').strip()

    # Base de la consulta SQL
    base_query = """
    SELECT 
        p.ID_Pago,
        CONCAT(c.Nombre, ' ', c.Apellido) AS Cliente,
        m.Tipo AS Membresia,
        m.Costo AS Precio,
        p.Fecha_Pago,
        p.Monto,
        p.Metodo_Pago,
        p.Estado,
        p.Referencia,
        p.Estado_Membresia,
        p.ID_Cliente,
        p.ID_Membresia
    FROM Pagos p
    JOIN Clientes c ON p.ID_Cliente = c.ID_Cliente
    JOIN Membresias m ON p.ID_Membresia = m.ID_Membresia
    """

    # Filtrar si hay un término de búsqueda
    if query_param:
        search_query = """
        WHERE c.Nombre LIKE %s
        OR c.Apellido LIKE %s
        OR m.Tipo LIKE %s
        OR p.Referencia LIKE %s
        """
        base_query += search_query
        search_value = f"%{query_param}%"
        cursor.execute(base_query, (search_value, search_value, search_value, search_value))
    else:
        cursor.execute(base_query)

    pagos = cursor.fetchall()

    # Calcular ingresos totales
    ingresos_query = """
    SELECT SUM(m.Costo) AS IngresosTotales
    FROM Pagos p
    JOIN Membresias m ON p.ID_Membresia = m.ID_Membresia
    WHERE p.Estado = 'Pagado'
    """
    cursor.execute(ingresos_query)
    ingresos_totales = cursor.fetchone()['IngresosTotales'] or 0  # Manejo de caso nulo

    cursor.close()
    db.close()

    return render_template('pagos.html', pagos=pagos, ingresos_totales=ingresos_totales, query=query_param)



@app.route('/pagos/delete/<int:id>', methods=['POST'])
def delete_pago(id):
    db = get_db_connection()
    cursor = db.cursor()

    # Verificar el estado de la membresía antes de eliminar
    cursor.execute("SELECT Estado_Membresia FROM pagos WHERE ID_Pago=%s", (id,))
    resultado = cursor.fetchone()

    if resultado:  # Si el pago existe
        estado_membresia = resultado[0]
        
        if estado_membresia in ['Activo', 'Validado']:
            flash("No se puede eliminar el pago, ya que la membresía está activa o validada.")
        else:
            # Si el estado es "Inactivo" o cualquier otro, se puede eliminar
            cursor.execute("DELETE FROM pagos WHERE ID_Pago=%s", (id,))
            db.commit()
            flash("Pago eliminado exitosamente.")
    else:
        flash("Pago no encontrado.")

    cursor.close()
    db.close()
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