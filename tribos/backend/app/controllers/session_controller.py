from flask_restful import Resource, reqparse
from app.database.connection import get_db
from app.utils import passwordEncrypt as pE
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')


class Session(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'logged_in_as': current_user}, 200

    def post(self):
        data = parser.parse_args()
        email = data['email']
        password = data['password']

        password = pE.password_encrypt(password)

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE  email='{email}'")
        username = cur.fetchone()

        if username is None:
            cur.close()
            return {'msg': 'Email não cadastrado'}, 401

        cur.execute(f"SELECT user_name FROM  users WHERE email='{email}' AND password='{password}'")
        user = cur.fetchone()
        cur.close()

        if user is None:
            return {'msg': 'Senha incorreta'}, 401

        access_token = create_access_token(identity=email)
        return {'access_token': access_token}, 200
