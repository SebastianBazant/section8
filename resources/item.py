import sqlite3
from sqlite3.dbapi2 import Connection
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Name cannot be blank!")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return{"massage": "Item not found"}, 404

    @jwt_required()
    def post(self, name):

        if ItemModel.find_by_name(name):
            # Something wrong with request
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name,  **data)
        try:
            item.save_to_db()
        except:
            # Something wrong wit the server
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

            return {"message": "Item deleted"}
        return {'message': 'Item not found.'}, 404

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item in None:

            item = ItemModel(name, **data)

        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
