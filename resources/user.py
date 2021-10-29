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
