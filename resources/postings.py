from flask import jsonify, Blueprint, abort, request
from flask_restful import (Resource, Api, reqparse,
                            fields, marshal,
                            marshal_with, url_for)
# from flask_login import login_required
import models


postings_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'username': fields.String,
 }

# posting = [
#   {'id': 1, 'title': 'Hello, World!', 'content': 'My first note!', 'username': 'sehee'},
# ]

def posting_or_404(posting_id):
    try:
        posting = models.Posting.get(models.Posting.id==postings_id)
    except models.Posting.DoesNotExist:
        abort(404)
    else:
        return posting

class PostingList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help="No titlekklkl provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'content',
            required=True,
            help="No content provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'username',
            required=True,
            help="No username provided",
            location=['form', 'json']
        )

        super().__init__()

    # @login_required
    def get(self):
        postings = [marshal(posting, postings_fields) for posting in models.Posting.select()]
        postings.append({'id': 0, 'title': 'Hello, World!', 'content': 'My first note!', 'username': 'sehee'})
        return {'postings' : postings}

    @marshal_with(postings_fields)
    def post(self):
        args = self.reqparse.parse_args()
        posting = models.Posting.create(**args)
        print(posting)
        return posting

class Posting(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help="No title provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'content',
            required=True,
            help="No content provided",
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(postings_fields)
    def get(self, id):
        return posting_or_404(id)

    @marshal_with(postings_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Posting.update(**args).where(models.Posting.id==id)
        query.execute()
        return (models.Posting.get(models.Posting.id==id), 200)

    def delete(self, id):
        query =  models.Posting.delete().where(models.Posting.id==id)
        query.execute()
        return 'resource was deleted'

postings_api = Blueprint('resources.postings', __name__)
api = Api(postings_api)

api.add_resource(
    PostingList,
    '/postings',
    endpoint='postings'
    )

api.add_resource(
    Posting,
    '/postings/<int:id>',
    endpoint='posting'
)
