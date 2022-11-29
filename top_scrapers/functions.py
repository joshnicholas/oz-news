from peewee import *
import re

db = SqliteDatabase('top_stuff/top.db')

class Post(Model):
    publication = CharField()

    # published_datetime = DateTimeField()

    scraped_datetime = DateTimeField()

    headline = CharField()
    url = CharField(unique=True)
    body = TextField()

    page_rank = IntegerField()

    class Meta:
        database = db

db.connect()

def top_sendo(objecto):
    try:
        Post.create(
        publication = objecto["publication"], 
        # published_datetime= objecto['published_datetime'],
        scraped_datetime= objecto['scraped_datetime'],

        headline = objecto['headline'],
        url = objecto['url'],

        page_rank = objecto['page_rank'])
    
        return True

    except Exception as e:
        print(f"{objecto['headline']} was already in")
        print(e)

        return False

def already_done(pubber):
    internal_list = []

    query = Post.select().where(Post.publication == pubber)

    for story in query:
        urlo = story.url
        internal_list.append(urlo)
    
    return internal_list


def remove_common(texto):
    texto = texto.replace("Sign up to receive an email with the top stories from Guardian Australia every morning", ' ')
    texto = texto.replace("Sign up to receive the top stories from Guardian Australia every morning", ' ')
    texto = texto.replace("Read more", '')
    texto = texto.replace("READ MORE", '')

    texto = re.sub(r'\.(?!\s|$)', '. ', texto)
    # texto = texto.replace(r'\b\.\b', '. ')
    return texto

    