# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

DB_ROUTE = 'data.db'


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field is required'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field is required'
    )

    def post(self):
        user_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(user_data['username']):
            return {'message': 'Username already in use'}, 400

        user = UserModel(**user_data)
        user.save_to_db()

        return {'message': 'User created'}, 201
