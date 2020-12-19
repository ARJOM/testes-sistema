from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.database.connection import get_db
from app.utils import passwordEncrypt as pE

# Informações que espera-se nos corpos das requisições
parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('user_name')
parser.add_argument('gender')
parser.add_argument('birthday')
parser.add_argument('password')


# Classe responsável por manter informações sobre usuários registrados
class User(Resource):
    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT email, user_name, gender, birthday FROM users WHERE email='{user_id}'")
        user = cur.fetchone()
        cur.close()

        if user is None:
            return {'msg': 'Não existe nenhum usuário registrado com o email informado'}, 404

        return user

    @jwt_required
    def delete(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{user_id}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Não existe nenhum usuário registrado com o email informado'}, 404

        cur.execute(f"DELETE FROM users WHERE email='{user_id}'")
        get_db().commit()
        cur.close()

        return {'msg': 'Usuário removido com sucesso'}, 200

    @jwt_required
    def put(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        username = data['user_name']
        gender = data['gender']
        birthday = data['birthday']
        password = data['password']

        password = pE.password_encrypt(password)

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{user_id}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Não existe nenhum usuário registrado com o email informado'}, 404

        cur.execute(f"UPDATE users SET user_name='{username}', gender={gender}, birthday='{birthday}', "
                    f"password='{password}' WHERE email='{user_id}'")
        get_db().commit()
        cur.close()

        return {'msg': 'Dados atualizados com sucesso'}, 201


# Classe responsável por listar usuários e cadastrar novos usuários
class UserList(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute("SELECT email, user_name, gender, birthday FROM users")
        users = cur.fetchall()
        cur.close()

        return users

    def post(self):
        data = parser.parse_args()
        email = data['email']
        username = data['user_name']
        gender = data['gender']
        birthday = data['birthday']
        password = data['password']

        password = pE.password_encrypt(password)

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{email}'")
        user = cur.fetchone()

        if user is not None:
            cur.close()
            return {'msg': 'Já existe um usuário registrado com esse email'}, 401

        cur.execute(f"INSERT INTO users(email, user_name, gender, birthday, password)"
                    f"VALUES ('{email}','{username}',{gender},'{birthday}','{password}')")
        get_db().commit()
        cur.close()

        return {'msg': 'Usuário registrado com sucesso'}, 201
