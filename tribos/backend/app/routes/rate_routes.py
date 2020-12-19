from app import api
from app.controllers.rate_controllers import *

api.add_resource(RateList, '/rates')
api.add_resource(Rate, '/rates/<string:user_id>/<int:item_id>')
