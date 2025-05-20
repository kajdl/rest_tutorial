from flask_restx import Resource
from flask import request

from api.users import users

# Resoure for a single user
# It has shared data coming from Users


class User(Resource):

    def get(self, id):
        for user in users:
            if id == user["id"]:
                return user

        return {"error": "user not found"}, 404

    def put(self, id):
        for i, user in enumerate(users):
            if id == user["id"]:
                users[i]["firstname"] = request.json["firstname"]
                users[i]["lastname"] = request.json["lastname"]
                return {"msg": "successfully updated user"}, 201
        return {"error": "user not found"}, 404
    
    def delete(self, id):
        for i, user in enumerate(users):
            if id == user["id"]:
                users.pop(i)
                return {"msg": "successfully deleted user"}, 201
        return {"error": "user not found"}, 404
