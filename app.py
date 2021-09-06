from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super cool and secret key'
api = Api(app)


# CREATE DB #
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(Stores, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
