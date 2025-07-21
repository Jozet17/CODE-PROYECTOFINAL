from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Esta parte se reemplazará por la base de datos
usuarios = {}  # Diccionario temporal: {correo: {"nombre": ..., "clave": ...}}

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
        fecha_nacimiento = request.form['fecha_nacimiento']

        # Verificación de edad
        from datetime import datetime, timedelta
        hoy = datetime.today()
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        edad = (hoy - fecha_nac).days // 365

        if edad < 18:
            flash('Debes ser mayor de edad para registrarte.', 'error')
            return render_template('registro.html', nombre=nombre, correo=correo)

        # Aquí va la verificación en base de datos
        if correo in usuarios:
            flash('Ese correo ya está registrado. Usa otro.', 'error')
            return render_template('registro.html', nombre=nombre, correo=correo)

        #  Aquí va el guardado en base de datos
        usuarios[correo] = {'nombre': nombre, 'clave': clave, 'correo': correo}
        flash('Registro exitoso. Ahora inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')

        user = usuarios.get(usuario)
        if user and user['clave'] == clave:
            session['usuario'] = usuario
            session['mensaje'] = 'Inicio de sesión exitoso'
            return redirect(url_for('panel_usuario'))
        else:
            error = 'Credenciales inválidas'
    return render_template('login.html', error=error)

@app.route('/recuperar', methods=['POST'])
def recuperar():
    correo = request.form.get('correo')

    #  Esto se cambiará por consulta a base de datos
    if correo in usuarios:
        flash('Se ha enviado un enlace de recuperación al correo.', 'success')
    else:
        flash('El correo no está registrado.', 'danger')
    return redirect(url_for('login'))

@app.route('/panel')
def panel_usuario():
    if 'usuario' not in session:
        flash('Primero inicia sesión.')
        return redirect(url_for('login'))
    return render_template('index2.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
