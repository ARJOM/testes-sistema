from app import api
from app.controllers.match_controllers import *

api.add_resource(Match, '/match')
