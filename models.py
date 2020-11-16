import datetime

from peewee import *

DATABASE = SqliteDatabase('notedb.sqlite')


class Posts(Model):
    title = CharField()
    content = CharField()
    username = CharField()
    created_by = ForeignKeyField(User, related_name='posts_set', null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Posts], safe=True)
    DATABASE.close()
