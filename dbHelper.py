from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Messages, Base
import logging

class dbHelper():
    def __init__(self):
        self.engine = create_engine('sqlite:///telebot.db')
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        # Init the logger
        self.logger = logging.getLogger('Telebot-Database')
        self.logger.setLevel(logging.DEBUG)

    def messageInsert(self, update):
        new_message = Messages(
                text=update.message.text,
                sender=update.update_id,
                chat=update.message.chat_id,
                date=update.message.date)
        self.session.add(new_message)
        self.session.commit()
