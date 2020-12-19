from app import api
from app.controllers.specific_item_controllers import *

api.add_resource(CategoryItem, '/categorys/items/<int:category_id>')
api.add_resource(RatedItem, '/rated/items/<string:user_id>')
api.add_resource(NotRatedItem, '/not/rated/items/<string:user_id>')
