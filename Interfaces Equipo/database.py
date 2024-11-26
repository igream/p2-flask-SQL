# Archivo de conexion a la base de datos

import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Gimnasio'
)
