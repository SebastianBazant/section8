import sqlite3

from flask_restful import reqparse, Resource
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True,
                          type=str,
                          help="Username cannot be blank!")

_user_parser.add_argument('password', required=True,
                          type=str,
                          help="Password cannot be blank!")


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

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


class UserLogin(Resource):

    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in dabase
        user = UserModel.find_by_username(data["username"])
        # check password
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token

            }, 200

        return {"message": "Invalid credentials"}, 401
        # create access token
        # create refresh token
