from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

usuarios_registrados = {}

@app.route('/')
def index():
    mensaje = session.pop('mensaje', None)
    return render_template('index.html', mensaje=mensaje)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']

        if correo in usuarios_registrados:
            flash('Ese correo ya está registrado. Usa otro.', 'error')
            return render_template('registro.html', nombre=nombre, correo=correo)

        usuarios_registrados[correo] = {'nombre': nombre, 'clave': clave}
        session['usuario'] = correo
        session['mensaje'] = 'Registro exitoso'
        return redirect(url_for('index'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        user = usuarios_registrados.get(usuario)

        if user and user['clave'] == clave:
            session['usuario'] = usuario
            session['mensaje'] = 'Inicio de sesión exitoso'
            return redirect(url_for('index'))
        else:
            error = 'Credenciales inválidas'
            return render_template('login.html', error=error, usuario=usuario)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session['mensaje'] = 'Sesión cerrada correctamente'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
