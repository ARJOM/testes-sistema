from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.database.connection import get_db

# Informações que espera-se nos corpos das requisições
parser = reqparse.RequestParser()
parser.add_argument('min_age')
parser.add_argument('max_age')
parser.add_argument('gender')


class Preference(Resource):
    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT p.min_age, p.max_age, p.gender as gender_id, g.gender_name as gender "
                    f"FROM preferences p JOIN genders g ON p.gender=g.gender_id "
                    f"WHERE user_email='{current_user}'")
        preference = cur.fetchone()
        cur.close()

        if preference is None:
            return {'msg': 'Usuário informado não possui preferências registradas'}, 404

        return preference, 200

    @jwt_required
    def post(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        min_age = data['min_age']
        max_age = data['max_age']
        gender = data['gender']

        cur = get_db().cursor()
        cur.execute(f"INSERT INTO preferences(user_email, min_age, max_age, gender) "
                    f"VALUES ('{user_id}',{min_age},{max_age},{gender})")
        get_db().commit()
        cur.close()

        return {'msg': 'Preferência registrada com sucesso'}, 201

    @jwt_required
    def put(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        min_age = data['min_age']
        max_age = data['max_age']
        gender = data['gender']

        cur = get_db().cursor()
        cur.execute(f"UPDATE preferences SET min_age={min_age}, max_age={max_age}, gender={gender} "
                    f"WHERE user_email='{current_user}'")
        get_db().commit()
        cur.close()

        return {'msg': 'Preferência atualizada com sucesso'}, 201


class PreferenceList(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute("SELECT * FROM preferences")
        preferences = cur.fetchall()
        cur.close()

        return preferences, 200
