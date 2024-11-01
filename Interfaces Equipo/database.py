# Formato de conector SQL, requiere driver python-sql
import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Gimnasio'
)
