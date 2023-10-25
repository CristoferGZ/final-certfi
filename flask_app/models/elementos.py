from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.usuarios import User


class Elemento:
    db_name = "mydb"
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.usuario_id = data.get('usuario_id')
        self.fecha_creacion = data.get('fecha_creacion')
        self.favoritos = []
    @classmethod
    def get_todos_elementos(cls):
        query = "SELECT * FROM elementos;"
        resultados = connectToMySQL('mydb').query_db(query)
        
        # Crea objetos Elemento con los resultados de la consulta y devuelve una lista de estos objetos
        elementos = []
        for resultado in resultados:
            elemento = cls(resultado)
            elementos.append(elemento)
        return elementos
    
    @classmethod
    def agregar_elemento(cls, nombre, usuario_id):
        query = "INSERT INTO elementos (nombre, usuario_id, fecha_creacion) VALUES (%(nombre)s, %(usuario_id)s, NOW());"
        data = {
            'nombre': nombre,
            'usuario_id': usuario_id
        }
        nuevo_elemento_id = connectToMySQL(cls.db_name).query_db(query, data)
        return nuevo_elemento_id
    @staticmethod
    def get_elementos_favoritos(usuario_id):
        query = "SELECT elementos.id, elementos.nombre, elementos.usuario_id, usuarios.nombre as creador_nombre, elementos.fecha_creacion FROM favoritos"
        query += " JOIN elementos ON favoritos.elemento_id = elementos.id"
        query += " JOIN usuarios ON elementos.usuario_id = usuarios.id"
        query += " WHERE favoritos.usuario_id = %(usuario_id)s;"
        data = {
            'usuario_id': usuario_id
        }
        results = connectToMySQL('mydb').query_db(query, data)
        elementos_favoritos = []
        if results:
            for row in results:
                elemento = {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'usuario_id': row['usuario_id'],
                    'creador_nombre': row['creador_nombre'],
                    'fecha_creacion': row['fecha_creacion']
                }
                elementos_favoritos.append(elemento)
        return elementos_favoritos


    @classmethod    
    def obtener_elementos_no_favoritos(cls, usuario_id):
        query = """
                SELECT elementos.id, elementos.nombre, usuarios.nombre AS creador_nombre, elementos.fecha_creacion
                FROM elementos
                JOIN usuarios ON elementos.usuario_id = usuarios.id
                WHERE elementos.id NOT IN (
                SELECT elemento_id
                FROM favoritos
                WHERE usuario_id = %(usuario_id)s
                );
        """
        data = {'usuario_id': usuario_id}
        return connectToMySQL('mydb').query_db(query, data)        
        
        
    @classmethod
    def obtener_elemento_por_id(cls, elemento_id):
        query = "SELECT * FROM elementos WHERE id = %(id)s;"
        data = {
            'id': elemento_id
        }
        result = connectToMySQL('mydb').query_db(query, data)

        # Verifica si se encontró el elemento con el ID proporcionado
        if result:
            elemento_data = result[0]
            return cls(elemento_data)  # Devuelve un solo objeto Elemento creado a partir de los datos de la base de datos
        else:
            return None         
    

    @staticmethod
    def obtener_elemento_con_favoritos(elemento_id):
        query = "SELECT elementos.*, usuarios.id as usuario_id, usuarios.nombre as usuario_nombre " \
                "FROM elementos " \
                "LEFT JOIN favoritos ON elementos.id = favoritos.elemento_id " \
                "LEFT JOIN usuarios ON favoritos.usuario_id = usuarios.id " \
                "WHERE elementos.id = %(id)s;"
        data = {
            'id': elemento_id
        }
        result = connectToMySQL('mydb').query_db(query, data)

        # Verifica si se encontró el elemento con el ID proporcionado
        if result:
            elemento_data = result[0]
            elemento = Elemento(elemento_data)
            favoritos = []
            for row in result:
                if row['usuario_id']:
                    usuario = User(row)  # Crea un objeto de usuario a partir de los datos recuperados
                    favoritos.append(usuario)
            elemento.favoritos = favoritos  # Asigna la lista de favoritos al atributo 'favoritos' del objeto elemento

            return elemento
        else:
            return None
        
    @staticmethod
    def obtener_nombres_favoritos_por_elemento_id(elemento_id):
        query = "SELECT usuarios.nombre as usuario_nombre " \
                "FROM favoritos " \
                "LEFT JOIN usuarios ON favoritos.usuario_id = usuarios.id " \
                "WHERE favoritos.elemento_id = %(id)s;"
        data = {
            'id': elemento_id
        }
        result = connectToMySQL('mydb').query_db(query, data)

        # Verifica si se encontraron usuarios que marcaron este elemento como favorito
        if result:
            nombres_favoritos = [row['usuario_nombre'] for row in result]
            return nombres_favoritos
        else:
            return []    
        
    @staticmethod
    def eliminar_elemento(elemento_id):
        # Eliminar las filas correspondientes en la tabla 'favoritos' primero
        query_eliminar_favoritos = "DELETE FROM favoritos WHERE elemento_id = %(elemento_id)s;"
        data_eliminar_favoritos = {
            'elemento_id': elemento_id
        }
        connectToMySQL('mydb').query_db(query_eliminar_favoritos, data_eliminar_favoritos)

        # Luego eliminar el elemento
        query_eliminar_elemento = "DELETE FROM elementos WHERE id = %(elemento_id)s;"
        data_eliminar_elemento = {
            'elemento_id': elemento_id
        }
        connectToMySQL('mydb').query_db(query_eliminar_elemento, data_eliminar_elemento)