from mongoengine import *


class Messages(Document):
    date = DateTimeField()
    message_id = IntField(primary_key=True, required=True, unique=True)
    update_id = IntField(required=True)
    from_user = IntField(required=True)
    from_chat = IntField(required=True)
    number_of_words = IntField(required=True)


class Users(Document):
    id = IntField(primary_key=True, required=True, unique=True)
    first_name = StringField(max_length=30, required=True)
    last_name = StringField(max_length=30)
    username = StringField(max_length=30)
    chats = ListField(IntField())


class Texts(Document):
    text = StringField(max_length=4096, required=True)
    date = DateTimeField()
    language = StringField(required=True, default='en')


class Chats(Document):
    chat_id = IntField(primary_key=True, required=True)
    type = StringField(max_length=30, required=True)
    title = StringField(max_length=40, required=True)
    users = ListField(IntField())
    date = DateTimeField()
