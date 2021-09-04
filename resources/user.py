import sqlite3
from flask_restful import Resource, reqparse


DB_ROUTE = 'data.db'


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, )).fetchone()
        connection.close()

        if result:
            return cls(*result)

        return None

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id, )).fetchone()
        connection.close()

        if result:
            return cls(*result)

        return None


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

        if User.find_by_username(user_data['username']):
            return {'message': 'Username already in use'}, 400

        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (user_data['username'], user_data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created'}, 201
