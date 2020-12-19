from app import api
from app.controllers.items_controllers import *

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')
