import sqlite3
from db import db

DB_ROUTE = 'data.db'


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        items = [item.json() for item in self.items.all()]
        return {'store_id': self.id, 'name': self.name, 'count': len(items), 'items': items}

    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
