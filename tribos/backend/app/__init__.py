from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '246135239ad0baf3657fa351f9ba8f77055cc4f9f5903d381c6864d61a45d5b72aac792ce748ed2ce9dc'
jwt = JWTManager(app)
api = Api(app)
CORS(app)

from app import router
