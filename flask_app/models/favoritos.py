from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

                        
class Favorito:
        db_name = "mydb" 
        def __init__(self,data):       
                self.id = data.get('id')
                self.usuario_id = data.get('usuario_id')
                self.elemento_id = data.get('elemento_id')
        
        @classmethod
        def get_favoritos(cls, usuario_id):
                query = "SELECT e.id, e.nombre FROM elementos e JOIN favoritos f ON e.id = f.elemento_id WHERE f.usuario_id = %(usuario_id)s;"
                data = {
                'usuario_id': usuario_id
                }
                favoritos = connectToMySQL('mydb').query_db(query, data)
                return favoritos
      
        @classmethod
        def agregar_favorito(cls, usuario_id, elemento_id):
                query = "INSERT INTO favoritos (usuario_id, elemento_id) VALUES (%(usuario_id)s, %(elemento_id)s);"
                data = {
                'usuario_id': usuario_id,
                'elemento_id': elemento_id
                }
                return connectToMySQL('mydb').query_db(query, data)


        @staticmethod
        def eliminar_favorito(elemento_id, usuario_id):
                query = "DELETE FROM favoritos WHERE elemento_id = %(elemento_id)s AND usuario_id = %(usuario_id)s;"
                data = {
                'elemento_id': elemento_id,
                'usuario_id': usuario_id
                }
                connectToMySQL('mydb').query_db(query, data)