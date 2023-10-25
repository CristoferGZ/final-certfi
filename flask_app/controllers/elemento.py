from flask import render_template,redirect, session,request, flash, url_for
from flask_app import app
from flask_app.models.elementos import Elemento
from flask_app.models.favoritos import Favorito
from flask_app.models.usuarios import User
from flask_app.config.mysqlconnection import connectToMySQL

import mysql.connector

@app.route('/agregar_elemento', methods=['GET', 'POST'])
def agregar_elemento():
    if request.method == 'POST':
        nombre = request.form['nombre']

        # Validar que el nombre del elemento sea más largo que 3 caracteres
        if len(nombre) <= 3:
            flash("El nombre del elemento debe tener más de 3 caracteres.", 'danger')
            return redirect('/agregar_elemento')

        # Intenta agregar el elemento a la base de datos
        try:
            nuevo_elemento_id = Elemento.agregar_elemento(nombre, session['usuario_id'])
            flash(f"Elemento '{nombre}' agregado exitosamente.", 'success')
        except Exception as e:
            print(e)  # Puedes imprimir el error para debuggear
            flash("Hubo un error al agregar el elemento. Inténtalo de nuevo.", 'danger')

        # Redirigir a la página de dashboard después de añadir el elemento
        return redirect('/dashboard')
    else:
        # Si es una solicitud GET, simplemente renderiza la plantilla para añadir elementos
        return render_template('agregar_elemento.html')



@app.route('/agregar_favorito/<int:elemento_id>', methods=['POST'])
def agregar_favorito(elemento_id):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        if Favorito.agregar_favorito(usuario_id, elemento_id):
            flash("Elemento añadido a favoritos exitosamente.", 'success')
        else:
            flash("Hubo un error al añadir el elemento a favoritos. Inténtalo de nuevo.", 'danger')

        # Redirigir a la página de donde vino el usuario (puedes cambiar esto a donde desees redirigir)
        return redirect(request.referrer or '/')
    else:
        return redirect('/')


@app.route('/eliminar_favorito/<int:elemento_id>', methods=['POST'])
def eliminar_favorito(elemento_id):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        
        # Lógica para eliminar el elemento favorito
        Favorito.eliminar_favorito(elemento_id, usuario_id)

        flash("Elemento eliminado de favoritos exitosamente.", 'success')
    else:
        flash("Debes iniciar sesión para realizar esta acción.", 'danger')

    # Redirige a la página de dashboard después de eliminar el elemento
    return redirect('/dashboard')


@app.route('/eliminar_elemento/<int:elemento_id>', methods=['POST'])
def eliminar_elemento(elemento_id):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        elemento = Elemento.obtener_elemento_por_id(elemento_id)

        # Verificar si el usuario de la sesión es el dueño del elemento
        if elemento and elemento.usuario_id == usuario_id:
            # Lógica para eliminar el elemento
            Elemento.eliminar_elemento(elemento_id)
            flash("Elemento eliminado exitosamente.", 'success')
        else:
            flash("No tienes permiso para eliminar este elemento.", 'danger')
    else:
        flash("Debes iniciar sesión para realizar esta acción.", 'danger')

    return redirect('/dashboard')


@app.route('/whish_item/<int:elemento_id>')
def ver_elemento(elemento_id):
    elemento = Elemento.obtener_elemento_por_id(elemento_id)
    nombres_favoritos = Elemento.obtener_nombres_favoritos_por_elemento_id(elemento_id)
    return render_template('show_elemento.html', elemento=elemento, nombres_favoritos=nombres_favoritos)