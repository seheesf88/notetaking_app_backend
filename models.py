import datetime

from peewee import *

DATABASE = SqliteDatabase('notedb.sqlite')


class Posting(Model):
    title = CharField()
    content = CharField()
    username = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Posting], safe=True)
    DATABASE.close()
