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
        if (len(q) == 0):
            new_chat = Chats(
                    chat_id=update.message.chat_id,
                    title=update.message.chat.title,
                    type=update.message.chat.type,
                    date=update.message.date
            )
            new_chat.save()
        else:
            q.update(add_to_set__users=update.message.from_user.id)


    def createUser(self, update):
        q = Users.objects(id=update.message.from_user.id)
        if len(q) == 0:
            new_user = Users(
                    id=update.message.from_user.id,
                    first_name=update.message.from_user.first_name,
                    last_name=update.message.from_user.last_name,
                    username=update.message.from_user.username,
                    chats=[update.message.chat_id]
            )
            new_user.save()
        else:
            q.update(add_to_set__chats=update.message.chat_id)


    def count(self, update, args):
        if args[0] == 'all':
            messages = Messages.objects(from_chat=update.message.chat.id)
            username = update.message.chat.title
        else:
            userSearch = Users.objects(first_name__iexact=' '.join(args), chats__contains=update.message.chat_id).only(
                'id','username','first_name').first()   if len(args) > 0 else update.message.from_user
            username = userSearch.username if userSearch.username else userSearch.first_name
            messages = Messages.objects(from_user=userSearch.id).only('text')

        return username, len(messages), self.countWords(messages)

    def countWords(self,messages):
        totalWords = 0
        for message in messages:
            totalWords += len(message.text.split())
        return totalWords
