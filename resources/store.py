import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

DB_ROUTE = 'data.db'


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            return {'store': store.json()}, 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if not store:
            return {'message': 'Store does not exist'}, 400
        try:
            store.delete()
        except:
            return {'message': 'Internal error'}, 500
        return {'message': 'Store removed'}, 200

    @jwt_required()
    def put(self, name):
        store = StoreModel.find_item_by_name(name)
        if not store:
            return {'message': 'Store not found'}, 404
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name',
            type=str,
            required=True,
            help='This field "name" cannot be left blank!'
        )
        data = parser.parse_args()
        for key in data:
            store.__setattr__(key, data[key])
        try:
            store.save_to_db()
        except:
            return {'message': 'Internal error'}, 500
        return store.json(), 200


class Stores(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.get_all()
        return {'count': len(stores), 'stores': [store.json() for store in stores]}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name',
            type=str,
            required=True,
            help='Name field must be unique'
        )
        data = parser.parse_args()
        store = StoreModel(**data)
        if StoreModel.find_item_by_name(data['name']):
            return {'message': 'Name must be unique'}, 400
        try:
            store.save_to_db()
        except:
            return {'message': 'Internal error'}, 500

        return store.json(), 201

