import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


DATABASE = SqliteDatabase('notedb.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


    @classmethod
    def create_user(cls, username, password):

        try:
            cls.select().where(
                (cls.username==username)
                ).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already Exists")

class Posting(Model):
    title = CharField()
    content = CharField()
    username = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Posting], safe=True)
    DATABASE.close()
