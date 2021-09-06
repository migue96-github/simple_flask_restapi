import sqlite3
from db import db

DB_ROUTE = 'data.db'


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # <table_name.primary_key>
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # connection = sqlite3.connect(DB_ROUTE)
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        #
        # result = cursor.execute(query, (name,)).fetchone()
        # connection.close()
        # if result:
        #     return cls(*result)
        # return None

    @classmethod
    def get_all(cls):
        return cls.query.all()
        # connection = sqlite3.connect(DB_ROUTE)
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        #
        # result = cursor.execute(query)
        # items = []
        # for item in result:
        #     items.append(cls(*item))
        # connection.close()
        # return items

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def insert(self):
    #     if self.find_item_by_name(self.name):
    #         return False
    #     connection = sqlite3.connect(DB_ROUTE)
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO items VALUES (?, ?)"
    #     cursor.execute(query, (self.name, self.price))
    #     connection.commit()
    #     connection.close()
    #
    #     return True

    # def update(self):
    #     if not self.find_item_by_name(self.name):
    #         return False
    #     connection = sqlite3.connect(DB_ROUTE)
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()
    #
    #     return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        # if not ItemModel.find_item_by_name(self.name):
        #     return False
        #
        # connection = sqlite3.connect(DB_ROUTE)
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (self.name,))
        # connection.commit()
        # connection.close()
        #
        # return True
