from peewee import *
from playhouse.postgres_ext import ArrayField

USER = ''
PASSWORD = ''
DB_NAME = ''

db_handle = PostgresqlDatabase(DB_NAME,
                               user=USER,
                               password=PASSWORD,
                               host='localhost',
                               port=5432)


class BaseModel(Model):
    class Meta:
        database = db_handle


class Image(BaseModel):
    feed_id = CharField(unique=True)
    images = ArrayField(TextField)

    class Meta:
        db_table = 'images'
        order_by = ('feed_id',)


class Text(BaseModel):
    feed_id = CharField(unique=True)
    text = TextField()

    class Meta:
        db_table = 'texts'
        order_by = ('feed_id',)


class Link(BaseModel):
    feed_id = CharField(unique=True)
    links = ArrayField(TextField)

    class Meta:
        db_table = 'links'
        order_by = ('feed_id',)
