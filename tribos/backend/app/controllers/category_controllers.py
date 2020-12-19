from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.database.connection import get_db

# Informações que espera-se nos corpos das requisições
parser = reqparse.RequestParser()
parser.add_argument('category_name')


class Category(Resource):
    def get(self, category_id):
        cur = get_db().cursor()
        cur.execute(f"SELECT category_name FROM categorys WHERE category_id={category_id}")
        category = cur.fetchone()
        cur.close()

        if category is None:
            return {'msg': 'Não existe nenhuma categoria registrada com o id informado'}, 404

        return category, 200

    @jwt_required
    def put(self, category_id):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute(f"SELECT category_name FROM categorys WHERE category_id={category_id}")
        category_name = cur.fetchone()

        if category_name is None:
            cur.close()
            return {'msg': 'Não existe nenhuma categoria registrada com o id informado'}, 404

        data = parser.parse_args()
        category_name = data['category_name']

        cur.execute(f"UPDATE categorys SET category_name='{category_name}' WHERE category_id={category_id}")
        get_db().commit()
        cur.close()

        return {'msg': 'Dados atualizados com sucesoo'}, 201

    @jwt_required
    def delete(self, category_id):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute(f"SELECT category_name FROM categorys WHERE category_id={category_id}")
        category = cur.fetchone()

        if category is None:
            cur.close()
            return {'msg': 'Não existe nenhuma categoria registrada com o id informado'}, 404

        cur.execute(f"DELETE FROM categorys WHERE category_id={category_id}")
        get_db().commit()
        cur.close()

        return {'msg': 'Categoria removida com sucesso'}, 200


class CategoryList(Resource):
    def get(self):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM categorys")
        categorys = cur.fetchall()
        cur.close()

        return categorys, 200

    # TODO permitir que apenas admninistradores criem novas categorias
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        category_name = data['category_name']

        cur.execute(f"INSERT INTO categorys(category_name) VALUES ('{category_name}')")
        get_db().commit()
        cur.close()

        return {'msg': 'Categoria registrada com sucesso'}, 201
