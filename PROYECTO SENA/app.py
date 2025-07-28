from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Carpeta de subida de fotos
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'imagenes', 'fotos_usuarios')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Diccionario temporal (simula base de datos)
usuarios = {}  # Estructura: {correo: {nombre, clave, correo, foto, otros datos}}

@app.route('/')
def index():
    mensaje = session.pop('mensaje', None)
    ruta_carrusel = os.path.join(app.static_folder, 'imagenes', 'carrusel')
    imagenes = [f for f in os.listdir(ruta_carrusel) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    imagenes.sort()
    return render_template('index.html', mensaje=mensaje, imagenes=imagenes)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        fecha_nacimiento = request.form['fecha_nacimiento']

        hoy = datetime.today()
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        edad = (hoy - fecha_nac).days // 365

        if edad < 18:
            flash('Debes ser mayor de edad para registrarte.', 'error')
            return render_template('registro.html', nombre=nombre, correo=correo)

        if correo in usuarios:
            flash('Ese correo ya está registrado.', 'error')
            return render_template('registro.html', nombre=nombre, correo=correo)

        usuarios[correo] = {
            'nombre': nombre,
            'clave': clave,
            'correo': correo,
            'fecha_nacimiento': fecha_nacimiento,
            'telefono': '',
            'direccion': '',
            'foto': ''
        }

        flash('¡Registro exitoso! Bienvenido a Pool Nene.', 'success')
        return redirect(url_for('index'))
    
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

    correo = session['usuario']
    usuario = usuarios.get(correo)

    if not usuario:
        flash('Usuario no encontrado.')
        return redirect(url_for('login'))

    return render_template('index2.html', usuario=usuario)


@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if 'usuario' not in session:
        flash('Primero inicia sesión')
        return redirect(url_for('login'))

    correo = session['usuario']
    user = usuarios.get(correo)

    if not user:
        flash('Usuario no encontrado')
        return redirect(url_for('panel_usuario'))

    user['nombre'] = request.form.get('nombre', user.get('nombre'))
    user['fecha_nacimiento'] = request.form.get('fecha_nacimiento', user.get('fecha_nacimiento'))
    user['telefono'] = request.form.get('telefono', user.get('telefono'))
    user['direccion'] = request.form.get('direccion', user.get('direccion'))

    if 'foto' in request.files:
        foto = request.files['foto']
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            ruta_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                foto.save(ruta_foto)
                user['foto'] = filename
                print("✅ Imagen guardada en:", ruta_foto)
                print("📸 Nombre archivo:", filename)
            except Exception as e:
                print("❌ Error al guardar imagen:", e)
        else:
            print("⚠️ No se subió una imagen válida")
    else:
        print("❌ Campo 'foto' no está en request.files")

    print("👤 Usuario actualizado:", user)

    flash('Perfil actualizado correctamente')
    return redirect(url_for('panel_usuario'))



@app.route('/ver_servicios')
def ver_servicios():
    return render_template('3casillas/Ver_servicios.html')

@app.route('/ver_eventos')
def ver_eventos():
    return render_template('3casillas/Ver_eventos.html')

@app.route('/ver_ofertas')
def ver_ofertas():
    return render_template('3casillas/Ver_ofertas.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
