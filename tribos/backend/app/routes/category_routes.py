from app import api
from app.controllers.category_controllers import *

api.add_resource(CategoryList, '/categorys')
api.add_resource(Category, '/categorys/<int:category_id>')
