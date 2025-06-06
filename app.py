import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from conexiones import get_admin_connection, get_user_connection

app = Flask(__name__)
app.secret_key = 'password'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        cnx = get_user_connection()
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT correo FROM login WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, (correo, contraseña))
        usuario = cursor.fetchone()

        cursor.close()
        cnx.close()

        if usuario:
            session['usuario'] = {'correo': usuario['correo']}
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/')
def inicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('base.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)