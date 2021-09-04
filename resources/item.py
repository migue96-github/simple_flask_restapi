import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

DB_ROUTE = 'data.db'


class Item(Resource):
    def get(self, name):
        item = Item.find_item_by_name(name)
        return {'item': item}, 200 if item else 404

    def delete(self, name):
        if not Item.find_item_by_name(name):
            return {'message': 'Item not found'}, 404

        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item removed'}, 200

    def put(self, name):
        if not Item.find_item_by_name(name):
            return {'message': 'Item not found'}, 404
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field "price" cannot be left blank!'
        )
        data = parser.parse_args()
        Item.update_item(name, data['price'])
        return Item.find_item_by_name(name), 200

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,)).fetchone()
        connection.close()
        if result:
            return {'name': result[0], 'price': result[1]}
        return None

    @classmethod
    def create_item(cls, name, price):
        if cls.find_item_by_name(name):
            return False
        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

        return True

    @classmethod
    def update_item(cls, name, price):
        if not cls.find_item_by_name(name):
            return False
        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()

        return True



class Items(Resource):
    def get(self):
        connection = sqlite3.connect(DB_ROUTE)
        cursor = connection.cursor()

        query = "SELECT * FROM items"

        result = cursor.execute(query)
        items = []
        for item in result:
            items.append({'name': item[0], 'price': item[1]})
        connection.close()
        return {'items': items}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field "price" cannot be left blank!'
        )
        parser.add_argument(
            'name',
            type=str,
            required=True,
            help='Name field must be unique'
        )
        item = parser.parse_args()
        if not Item.create_item(item['name'], item['price']):
            return {'message': 'Name must be unique'}, 400

        return Item.find_item_by_name(item['name']), 201

