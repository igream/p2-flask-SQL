# Genera registros SQL manualmente para la base de datos del gimnasio

from werkzeug.security import generate_password_hash
print("Definir sentencia SQL para registrar un administrador")
user = input("Inserta el nombre de usuario: ")
password = input("Inserta la contraseña a encriptar: ")
hash_password = generate_password_hash(password)
print("Pega este comando SQL: ")
print(f"INSERT INTO Administradores (User, Password) VALUES ('{user}', '{hash_password}');")

# Contraseñas actuales
# user: admin1 password: contrasena1

# Se recomienda crear un ambiente virtual para ello, esto es solo código fuente
## Nota: Esta versión no contiene hash para las contraseñas, por lo que no se debe usar hash para registrar administradores por tema de versiones de werkzeug(Requerida 3.0.1) con PythonAnyWhere(2.0.1)
