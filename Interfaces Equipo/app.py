from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import connect, Error

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.secret_key = 'your_secret_key'

# Conexión a la base de datos MySQL
def get_db_connection():
    return connect(
        host="localhost",
        user="root",
        password="",
        database="Gimnasio"
    )

# Página principal con enlaces a cada tabla
@app.route('/')
def index():
    print("Accediendo a la ruta principal")
    return render_template('index.html')

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
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""UPDATE Clases 
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

@app.route('/clientes/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = %s", (id,))
        db.commit()
        flash("Cliente eliminado exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('clientes'))

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
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Clases (Nombre_Clase, Descripcion, Instructor, Hora, Capacidad) 
            VALUES (%s, %s, %s, %s, %s)""",
            (nombre, descripcion, instructor, hora, capacidad))
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
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Membresias (Tipo, Costo, Duracion, Descripcion) VALUES (%s, %s, %s, %s)",
                       (tipo, costo, duracion, descripcion))
        db.commit()
        flash("Membresía agregada exitosamente.")
    except Error as e:
        flash(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('membresias'))

@app.route('/membresias/delete/<int:id>', methods=['GET'])
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