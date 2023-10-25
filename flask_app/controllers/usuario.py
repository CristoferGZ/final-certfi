from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuarios import User
from flask_app.models.elementos import Elemento
from flask_app.models.favoritos import Favorito
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validar_registro(request.form):
        return redirect('/')
    else:
        hashed_password = bcrypt.generate_password_hash(request.form['contraseña'])
        data = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'contraseña': hashed_password
        }
        User.registrar_usuario(data)
        flash("Registro exitoso. ¡Inicia sesión!", 'register_success')
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user_data = {
        'email': request.form['email'],
        'contraseña': request.form['contraseña']
    }
    user = User.login_usuario(user_data)
    if user:
        session['usuario_id'] = user.id
        session['usuario_nombre'] = user.nombre  # Guarda el nombre del usuario en la sesión
        
        return redirect('/dashboard')  # Reemplaza '/dashboard' con la ruta a la página de inicio del usuario autenticado
    else:
        return redirect('/')
    
    
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' in session:
        elements =Elemento.get_todos_elementos()
        usuario_id_sesion = session['usuario_id']
        elementos_favoritos = Elemento.get_elementos_favoritos(usuario_id_sesion)
        elementos_no_favoritos = Elemento.obtener_elementos_no_favoritos(usuario_id_sesion)
        return render_template("dashboard.html", usuario_id_sesion=usuario_id_sesion, elementos_favoritos=elementos_favoritos, elementos_no_favoritos=elementos_no_favoritos, elementos = elements)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')