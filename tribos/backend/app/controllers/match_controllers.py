from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app.database.connection import get_db
from app.utils import getAge as gA
from app.utils import getSimilarity as gS


class Match(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        cur = get_db().cursor()
        cur.execute(f"SELECT * FROM users_preferences "
                    f"WHERE email='{current_user}'")
        user = cur.fetchone()

        if user is None:
            cur.close()
            return {'msg': 'Não existe nenhum usuário registrado com o email informado'}, 404

        user_age = gA.get_age(user['birthday'])
        user_min = user['min_age']
        user_max = user['max_age']
        user_wanted = user['wanted_gender']
        user_gender = user['gender']

        cur.execute(f"SELECT * FROM users_preferences WHERE email!='{current_user}'")
        users = cur.fetchall()

        matches = []

        for match in users:
            match_age = gA.get_age(match['birthday'])
            match_min = match['min_age']
            match_max = match['max_age']
            match_wanted = match['wanted_gender']
            match_gender = match['gender']
            # Verifica se as idades batem
            if user_max > match_age > user_min and match_max > user_age > match_min:
                # Verifica se os gêneros procurados betem
                if user_wanted == 3 and (match_wanted == user_gender or match_wanted == 3):
                    matches.append(match['email'])
                # Verifica se os gêneros procurados betem
                elif user_wanted == match_gender and match_wanted == user_gender:
                    matches.append(match['email'])

        base_rates = {current_user: {}}
        cur.execute(f"SELECT item, rate FROM rates WHERE user_email='{current_user}'")
        rates = cur.fetchall()
        for rate in rates:
            base_rates[current_user][rate['item']] = rate['rate']

        for email in matches:
            base_rates[email] = {}
            cur.execute(f"SELECT item, rate FROM rates WHERE user_email='{email}'")
            rates = cur.fetchall()
            for rate in rates:
                base_rates[email][rate['item']] = rate['rate']

        cur.close()

        recommendations = gS.get_similarity(base_rates, current_user)
        return recommendations
