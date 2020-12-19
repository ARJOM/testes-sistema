from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.database.connection import get_db

# Informações que espera-se nos corpos das requisições
parser = reqparse.RequestParser()
parser.add_argument('item_name')
parser.add_argument('category_id')


class Item(Resource):
    def get(self, item_id):
        cur = get_db().cursor()
        cur.execute(f"SELECT i.item_id, i.item_name, i.category, c.category_name "
                    f"FROM items i JOIN categorys c ON i.category = c.category_id "
                    f"WHERE i.item_id={item_id}")
        item = cur.fetchone()
        cur.close()

        return item, 200

    @jwt_required
    def put(self, item_id):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        data = parser.parse_args()
        item_name = data['item_name']
        category_id = data['category_id']

        cur.execute(f"UPDATE items SET item_name='{item_name}', category={category_id} WHERE item_id={item_id}")
        get_db().commit()
        cur.close()

        return {'msg': 'Dados atualizados com sucesso'}, 201

    @jwt_required
    def delete(self, item_id):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT user_name FROM users WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            return {'msg': 'Usuário não está autorizado a acessar informações solicitadas'}, 401

        cur.execute(f"SELECT item_name FROM items WHERE item_id={item_id}")
        category = cur.fetchone()

        if category is None:
            cur.close()
            return {'msg': 'Não existe nenhum item registrada com o id informado'}, 404

        cur.execute(f"DELETE FROM items WHERE item_id={item_id}")
        get_db().commit()
        cur.close()

        return {'msg': 'Item removido com sucesso'}, 200


class ItemList(Resource):
    def get(self):
        cur = get_db().cursor()
        cur.execute("SELECT i.item_id, i.item_name, i.category, c.category_name "
                    "FROM items i JOIN categorys c on i.category = c.category_id")
        items = cur.fetchall()
        cur.close()

        return items, 200

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
        item_name = data['item_name']
        category_id = data['category_id']

        cur.execute(f"INSERT INTO items(item_name, category) VALUES ('{item_name}',{category_id})")
        get_db().commit()
        cur.close()

        return {'msg': 'Item registrado com sucesso'}, 201
