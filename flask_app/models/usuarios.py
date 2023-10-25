from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db_name = "mydb"
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.email = data.get('email')
        self.contraseña = data.get('contraseña')
        self.fecha_registro = data.get('fecha_registro')
    
    @classmethod
    def registrar_usuario(cls, data):
        query = "INSERT INTO usuarios (nombre, email, contraseña, fecha_registro) VALUES (%(nombre)s, %(email)s, %(contraseña)s, NOW());"
        return connectToMySQL('mydb').query_db(query, data)

    @staticmethod
    def validar_registro(usuario_data):
        is_valid = True
        if len(usuario_data['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(usuario_data['email']):
            flash("Email inválido", 'register')
            is_valid = False
        if len(usuario_data['contraseña']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", 'register')
            is_valid = False
        if usuario_data['contraseña'] != usuario_data['confirm_password']:
            flash("Las contraseñas no coinciden", 'register')
            is_valid = False
        return is_valid

    @classmethod
    def login_usuario(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL('mydb').query_db(query, data)
        if len(result) > 0:
            if bcrypt.check_password_hash(result[0]['contraseña'], data['contraseña']):
                return cls(result[0])
        flash("Credenciales inválidas", 'login')
        return False