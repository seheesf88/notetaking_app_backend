import json
from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                            fields, marshal,
                            marshal_with, url_for)


from flask_login import login_user, logout_user
from flask_bcrypt import check_password_hash

import models

## define our response fields
user_fields = {
    'id' : fields.Integer,
    'username': fields.String,
}

def user_or_404(id):
    try:
        user = models.User.get(models.User.id == id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help="no Username provided",
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'password',
            required=True,
            help="no password provided",
            location=['form', 'json']
            )

        super().__init__()

    def get(self):
        users = [marshal(user, user_fields) for user in models.User.select()]
        return {"users" : users}, 200


    def post(self):
        args = self.reqparse.parse_args()
        user = models.User.create_user(username=args['username'], password=args['password'])
        login_user(user)
        return marshal(user, user_fields), 201

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=False,
            help='no username provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'password',
            required=False,
            help='no password provided',
            location=['form', 'json']
            )

        super().__init__()

    @marshal_with(user_fields)
    def get(self, id):
        return user_or_404(id)

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id==id)
        query.execute()
        return (models.User.get(models.User.id==id), 200)

    def delete(self, id):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return 'your account is removed'



class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='no username provided',
            location=['form', 'json']
            )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='no password provided',
            location=['form', 'json']
            )

        super().__init__()

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()

        try:
            user = models.User.get(models.User.username == args["username"])
        except models.DoesNotExist:
            return "fail login"
        else:
            if check_password_hash(user.password, args["password"]):
                login_user(user)
                return user
            else:
                return "fail login"

    def delete(self):
        logout_user()
        return "logout successful"



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)

api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)

api.add_resource(
    Login,
    '/users/login',
    endpoint='login'
)
