from peewee import *

db = SqliteDatabase('data/news.db')

class Post(Model):
    publication = CharField()

    # published_datetime = DateTimeField()
    scraped_datetime = DateTimeField()

    headline = CharField()
    url = CharField()
    body = TextField()

    page_rank = IntegerField()

    class Meta:
        database = db

db.connect()

db.create_tables([Post])