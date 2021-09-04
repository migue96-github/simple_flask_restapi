from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
app.secret_key = 'super cool and secret key'
api = Api(app)
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)