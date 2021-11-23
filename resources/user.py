import sqlite3

from flask_restful import reqparse, Resource
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        type=str,
                        help="Username cannot be blank!")

    parser.add_argument('password', required=True,
                        type=str,
                        help="Password cannot be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succcessfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(clas, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{"message": "User not found"}, 404
        user.delete_from_db()
        return{"message": "User deleted"}, 200
