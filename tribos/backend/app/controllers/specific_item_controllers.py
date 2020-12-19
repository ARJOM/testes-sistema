from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app.database.connection import get_db


class CategoryItem(Resource):
    def get(self, category_id):
        cur = get_db().cursor()
        cur.execute(f"SELECT i.item_id, i.item_name, c.category_name "
                    f"FROM items i JOIN categorys c on i.category = c.category_id "
                    f"WHERE category={category_id}")
        items = cur.fetchall()
        cur.close()

        return items, 200


class RatedItem(Resource):
    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()

        if current_user != user_id:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute(f"SELECT r.item, i.item_name, r.user_email, r.rate "
                    f"FROM rates r, items i "
                    f"WHERE r.item=i.item_id AND r.user_email='{current_user}'")
        rated = cur.fetchall()
        cur.close()

        return rated, 200


class NotRatedItem(Resource):
    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()

        if current_user != user_id:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute(f"SELECT * "
                    f"FROM items "
                    f"WHERE item_id NOT IN "
                    f"(SELECT item FROM rates WHERE user_email='{current_user}')")
        not_rated = cur.fetchall()
        cur.close()

        return not_rated, 200
