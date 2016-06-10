import logging

from mongoengine import connect

from models import Messages, Chats, Users


class dbHelper(object):
    def __init__(self):

        connect('telebot')

        # Init the logger
        self.logger = logging.getLogger('Telebot-Database')
        self.logger.setLevel(logging.DEBUG)

    def messageInsert(self, update):
        self.createChat(update)
        self.createUser(update)
        new_message = Messages(
                text=update.message.text,
                from_user=update.message.from_user.id,
                from_chat=update.message.chat_id,
                date=update.message.date,
                message_id=update.message.message_id,
                update_id=update.update_id)
        new_message.save()

    def createChat(self, update):
        q = Chats.objects(chat_id__exists=update.message.chat_id)
        print(q)
        if (len(q) == 0):
            new_chat = Chats(
                    chat_id=update.message.chat_id,
                    title=update.message.chat.title,
                    type=update.message.chat.type,
                    date=update.message.date
            )
            new_chat.save()

    def createUser(self, update):
        q = Users.objects(user_id=update.message.from_user.id)
        if len(q) == 0:
            new_user = Users(
                    user_id=update.message.from_user.id,
                    first_name=update.message.from_user.first_name,
                    last_name=update.message.from_user.last_name,
                    username=update.message.from_user.username,
                    chats = [update.message.chat_id]
            )
            new_user.save()

    def count(self, update, args):
        userSearch = Users.objects(first_name__iexact=args,chats__contains=update.message.chat_id).only('user_id').first() # if len(args) > 0 else update.message.from_user.id
        print("\n fuck \n fuck")
        print(userSearch)
        print (''.join(userSearch))
        # messagesQ = Messages.objects()
        # count = len(messagesQ)
        # words = 0
        # for message in q:
        #   words += len(message.text.split())
        return ("fuck", "fuck", "fuck")
