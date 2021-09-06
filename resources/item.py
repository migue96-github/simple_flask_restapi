import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

DB_ROUTE = 'data.db'


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {'item': item.json()}, 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'message': 'Item does not exist'}, 400
        try:
            item.delete()
        except:
            return {'message': 'Internal error'}, 500
        return {'message': 'Item removed'}, 200

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'message': 'Item not found'}, 404
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field "price" cannot be left blank!'
        )
        parser.add_argument(
            'store_id',
            type=int,
            required=True,
            help='Must be included'
        )
        data = parser.parse_args()
        for key in data:
            item.__setattr__(key, data[key])
        try:
            item.save_to_db()
        except:
            return {'message': 'Internal error'}, 500
        return item.json(), 200


class Items(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.get_all()
        return {'count': len(items), 'items': [item.json() for item in items]}

    @jwt_required()
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
        parser.add_argument(
            'store_id',
            type=int,
            required=True,
            help='Must be included'
        )
        data = parser.parse_args()
        item = ItemModel(**data)
        if ItemModel.find_item_by_name(data['name']):
            return {'message': 'Name must be unique'}, 400
        try:
            item.save_to_db()
        except:
            return {'message': 'Internal error'}, 500

        return item.json(), 201

