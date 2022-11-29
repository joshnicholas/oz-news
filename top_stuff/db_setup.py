from peewee import *

db = SqliteDatabase('top_stuff/top.db')

class Post(Model):
    publication = CharField()

    # published_datetime = DateTimeField()
    scraped_datetime = DateTimeField()

    headline = CharField()
    url = CharField()

    page_rank = IntegerField()

    class Meta:
        database = db

db.connect()

db.create_tables([Post])