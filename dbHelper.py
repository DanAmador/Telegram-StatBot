import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Messages, Base, Chats, Users


class dbHelper(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///telebot.db')

        Base.metadata.bind = self.engine
        Base.metadata.create_all()
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        # Init the logger
        self.logger = logging.getLogger('Telebot-Database')
        self.logger.setLevel(logging.DEBUG)

    def messageInsert(self, update):
        self.createChat(update)
        self.createUser(update)
        new_message = Messages(
                text=update.message.text,
                sender=update.message.from_user.id,
                chatId=update.message.chat_id,
                date=update.message.date)
        self.session.add(new_message)
        self.session.commit()

    def createChat(self, update):
        q = self.session.query(Chats).filter_by(id=update.message.chat_id).first()
        if (q == None):
            new_chat = Chats(
                    id=update.message.chat_id,
                    title=update.message.chat.title,
                    type=update.message.chat.type,
                    date=update.message.date
            )
            self.session.add(new_chat)
            self.session.commit()

    def createUser(self, update):
        q = self.session.query(Users).filter_by(id=update.message.from_user.id).first()
        if q == None:
            new_user = Users(
                    id=update.message.from_user.id,
                    first_name=update.message.from_user.first_name,
                    last_name=update.message.from_user.last_name,

            )
            self.session.add(new_user)
            self.session.commit()
