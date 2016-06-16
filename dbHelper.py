import logging

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
        new_message = Messages(
                text=update.message.text,
                date=update.message.date,
                from_user=update.message.from_user.id,
                from_chat=update.message.chat_id,
                message_id=update.message.message_id,
                update_id=update.update_id,
                number_of_words=len(update.message.text.split()))

        new_text = Texts(text=update.message.text,
                         date=update.message.date)
        new_text.save()
        new_message.save()

    def createChat(self, update):
        q = Chats.objects(chat_id=update.message.chat_id)
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
                    'id', 'username', 'first_name').first() if len(args) > 0 else update.message.from_user
            username = userSearch.username if userSearch.username else userSearch.first_name
            messages = Messages.objects(from_user=userSearch.id).only('text')

        return username, len(messages), self.countWords(messages)

    def countWords(self, messages):
        totalWords = 0
        for message in messages:
            totalWords += int(message.number_of_words)
        return totalWords

    def minMaxStats(self, update, users_in_convversation):
        allMessages = Messages.objects(from_chat=update.message.chat_id).only('from_user', 'number_of_words')
        totalMessages = float(len(allMessages))
        user_stats = []
        totalWords = 0
        for user in users_in_convversation:
            messages = Messages.objects(from_chat=update.message.chat_id, from_user=user).only('from_user',
                                                                                               'number_of_words')
            messagesPerUser = float(len(messages))
            wordsPerUser = self.countWords(messages)
            totalWords += wordsPerUser

            user_stats.append({
                'user': user,
                'number_of_messages': messagesPerUser,
                'conversation_percentage': "{0:.2f}".format((messagesPerUser / totalMessages) * 100),
                'number_of_words': wordsPerUser
            })
        return {'total_words': totalWords, 'total_messages': totalMessages, 'user_stats': user_stats}

    def minMaxParse(self, update):
        users = Chats.objects(chat_id=update.message.chat_id).only('users').first().users
        user_stats_dict = self.minMaxStats(update, users)
        user_stats = user_stats_dict['user_stats']
        max_messages = max(user_stats, key=lambda x: x['number_of_messages'])
        max_words = max(user_stats, key=lambda x: x['number_of_words'])

        return "Most messages sent:  %s with %d messages from a total of %d \nMost words used: %s with %d words from a total of %d" % (
            self.getUserName(max_messages['user']), max_messages['number_of_messages'],
            user_stats_dict['total_messages'],
            self.getUserName(max_words['user']), max_words['number_of_words'], user_stats_dict['total_words'])

    def getUserName(self, id):
        user_object = Users.objects(id=id).only('first_name', 'username').first()
        return_string = user_object.username if user_object.username else user_object.first_name
        return str(return_string)
