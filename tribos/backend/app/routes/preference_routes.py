from app import api
from app.controllers.preference_controllers import *

api.add_resource(Preference, '/preferences/<string:user_id>')
api.add_resource(PreferenceList, '/preferences')
