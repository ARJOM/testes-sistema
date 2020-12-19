from app import api
from app.controllers.session_controller import *

# Adicionando rotas
api.add_resource(Session, '/session')
