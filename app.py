import mysql.connector

def get_db_connection():
    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        port= 3307,
        database='obligatorio'
    )
    return cnx