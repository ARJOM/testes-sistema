from app import api
from app.controllers.user_controller import *

# Adicionando rotas
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<string:user_id>')
