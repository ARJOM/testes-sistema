from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.database.connection import get_db

# Informações que espera-se nos corpos das requisições
parser = reqparse.RequestParser()
parser.add_argument('rate')


class Rate(Resource):
    def get(self, user_id, item_id):
        cur = get_db().cursor()
        cur.execute(f"SELECT r.user_email, r.item, i.item_name, r.rate FROM rates r JOIN items i ON r.item=i.item_id "
                    f"WHERE r.item={item_id} AND r.user_email='{user_id}'")
        rate = cur.fetchone()
        cur.close()

        return rate, 200

    @jwt_required
    def put(self, user_id, item_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        rate = data['rate']

        cur.execute(f"UPDATE rates SET rate={rate} WHERE item={item_id} AND user_email='{current_user}'")
        get_db().commit()
        cur.close()

        return {'msg': 'Dados atualizados com sucesso'}, 201

    @jwt_required
    def post(self, user_id, item_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        rate = data['rate']

        cur.execute(f"INSERT INTO rates(user_email, item, rate) VALUES ('{current_user}', {item_id}, {rate})")
        get_db().commit()
        cur.close()

        return {'msg': 'Avaliação registrada com sucesso'}, 201


class RateList(Resource):
    def get(self):
        cur = get_db().cursor()
        cur.execute("SELECT r.user_email, r.item, i.item_name, r.rate FROM rates r JOIN items i ON r.item=i.item_id")
        rates = cur.fetchall()
        cur.close()

        return rates, 200
