import logging

from langdetect import detect
from mongoengine import connect

from models import Messages, Chats, Users, Texts


class dbHelper(object):
    def __init__(self):

        connect('telebot')

        # Init the logger
        self.logger = logging.getLogger('Telebot-Database')
        self.logger.setLevel(logging.DEBUG)

    def messageInsert(self, update):
        self.createChat(update)
        self.createUser(update)

        msg = update.message
        new_message = Messages(
            date=msg.date,
            from_user=msg.from_user.id,
            from_chat=msg.chat_id,
            message_id=msg.message_id,
            update_id=update.update_id,
            number_of_words=len(msg.text.split())
        )
        new_text = Texts(
            text=msg.text,
            date=msg.date,
            language=detect(msg.text)
        )
        new_text.save()
        new_message.save()

    def createChat(self, update):
        msg = update.message
        q = Chats.objects(chat_id=msg.chat_id)
        if not q:
            new_chat = Chats(
                chat_id=msg.chat_id,
                title=msg.chat.title,
                type=msg.chat.type,
                date=msg.date
            )
            new_chat.save()
        else:
            q.update(add_to_set__users=update.message.from_user.id)

    def createUser(self, update):
        msg = update.message
        q = Users.objects(id=msg.from_user.id)
        if not q:
            new_user = Users(
                id=msg.from_user.id,
                first_name=msg.from_user.first_name,
                last_name=msg.from_user.last_name,
                username=msg.from_user.username,
                chats=[msg.chat_id]
            )
            new_user.save()
        else:
            q.update(add_to_set__chats=update.message.chat_id)

    def count(self, update, args):
        msg = update.message
        if args[0] is 'all':
            messages = Messages.objects(from_chat=msg.chat.id)
            username = msg.chat.title
        else:
            userSearch = Users.objects(
                first_name__iexact=' '.join(args),
                chats__contains=msg.chat_id
            ).only('id', 'username', 'first_name')\
             .first() if len(args) > 0 else update.message.from_user
            username = userSearch.username if userSearch.username else userSearch.first_name
            messages = Messages.objects(from_user=userSearch.id).only('text')

        return username, len(messages), self.countWords(messages)

    def countWords(self, messages):
        totalWords = 0
        for message in messages:
            totalWords += int(message.number_of_words)
        return totalWords

    def minMaxStats(self, update, users_in_convversation):
        msg = update.message
        allMessages = Messages.objects(
            from_chat=msg.chat_id
        ).only('from_user', 'number_of_words')
        totalMessages = float(len(allMessages))
        user_stats = []
        totalWords = 0
        for user in users_in_convversation:
            messages = Messages.objects(
                from_chat=msg.chat_id,
                from_user=user
            ).only('from_user', 'number_of_words')
            messagesPerUser = float(len(messages))
            wordsPerUser = self.countWords(messages)
            totalWords += wordsPerUser
            conv_percentage = (messagesPerUser / totalMessages) * 100

            user_stats.append({
                'user': user,
                'number_of_messages': messagesPerUser,
                'conversation_percentage': "{0:.2f}".format(conv_percentage),
                'number_of_words': wordsPerUser
            })
        return {
            'total_words': totalWords,
            'total_messages': totalMessages,
            'user_stats': user_stats
        }

    def minMaxParse(self, update):
        users = Chats.objects(chat_id=update.message.chat_id).only('users').first().users
        user_stats_dict = self.minMaxStats(update, users)
        user_stats = user_stats_dict['user_stats']
        max_messages = max(user_stats, key=lambda x: x['number_of_messages'])
        max_words = max(user_stats, key=lambda x: x['number_of_words'])
        msg_template = ("Most messages sent: {user} with {user_msg} messages from a total of"
                        "{total_msg}\nMost words used: {user_maxw} with {user_words} words "
                        "from a total of {total_words}")

        return msg_template.format(
            user=self.getUserName(max_messages['user']),
            user_msg=max_messages['number_of_messages'],
            total_msg=user_stats_dict['total_messages'],
            user_maxw=self.getUserName(max_words['user']),
            user_words=max_words['number_of_words'],
            total_words=user_stats_dict['total_words']
        )

    def getUserName(self, id):
        user_object = Users.objects(id=id).only('first_name', 'username').first()
        username = user_object.username
        first_name = user_object.first_name
        return str(username) if username else str(first_name)
