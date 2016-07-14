import logging
import os

from langdetect import DetectorFactory, detect
from mongoengine import connect
from models import Messages, Chats, Users, Texts


class Dbhelper(object):
    def __init__(self):
        DetectorFactory.seed = 0
        connect('telebot')

        # Init the logger
        self.logger = logging.getLogger('Telebot-Database')
        self.logger.setLevel(logging.DEBUG)

    def insert_message(self, update):
        self.create_chat(update)
        self.create_user(update)

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

    @staticmethod
    def create_chat(update):
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

    @staticmethod
    def create_user(update):
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
            if len(args):
                user = Users.objects(
                        first_name__iexact=' '.join(args),
                        chats__contains=msg.chat_id
                ).only('id', 'username', 'first_name').first()
            else:
                msg.from_user
            username = user.username if user.username else user.first_name
            messages = Messages.objects(from_user=user.id).only('text')

        return username, len(messages), self.count_words(messages)

    @staticmethod
    def count_words(messages):
        totalWords = 0
        for message in messages:
            totalWords += int(message.number_of_words)
        return totalWords

    def get_chat_stats(self, update, users_in_conversation):
        msg = update.message
        all_messages = Messages.objects(
                from_chat=msg.chat_id
        ).only('from_user', 'number_of_words')
        total_messages = float(len(all_messages))
        user_stats = []
        total_words = 0
        for user in users_in_conversation:
            messages = Messages.objects(
                    from_chat=msg.chat_id,
                    from_user=user
            ).only('from_user', 'number_of_words')
            messages_per_user = float(len(messages))
            words_per_user = self.count_words(messages)
            total_words += words_per_user
            conv_percentage = (messages_per_user / total_messages) * 100

            user_stats.append({
                'user': user,
                'number_of_messages': messages_per_user,
                'conversation_percentage': "{0:.2f}".format(conv_percentage),
                'number_of_words': words_per_user
            })
        return {
            'total_words': total_words,
            'total_messages': total_messages,
            'user_stats': user_stats
        }

    def parse_chat_stats(self, update):
        users = Chats.objects(chat_id=update.message.chat_id).only('users').first().users
        user_stats_dict = self.get_chat_stats(update, users)
        user_stats = user_stats_dict['user_stats']
        max_messages = max(user_stats, key=lambda x: x['number_of_messages'])
        max_words = max(user_stats, key=lambda x: x['number_of_words'])
        msg_template = ("""Most messages sent: {user} with {user_msg} messages from a total of {total_msg}
Most words used: {user_maxw} with {user_words} words from a total of {total_words}""")

        return msg_template.format(
                user=self.get_user_name(max_messages['user']),
                user_msg=int(max_messages['number_of_messages']),
                total_msg=int(user_stats_dict['total_messages']),
                user_maxw=self.get_user_name(max_words['user']),
                user_words=int(max_words['number_of_words']),
                total_words=user_stats_dict['total_words']
        )

    @staticmethod
    def get_user_name(user_id):
        user_object = Users.objects(id=user_id).only('first_name', 'username').first()
        username = user_object.username
        first_name = user_object.first_name
        return str(username) if username else str(first_name)

    @staticmethod
    def get_languages_message_count():
        languages = Texts.objects().only('language').distinct('language')
        count = {}
        for language in languages:
            count[language] = Texts.objects(language=language).count()
        return count

    @staticmethod
    def index_messages_by_language(language, indexed=False):
        texts_by_language = Texts.objects(language=language, indexed=indexed)
        message_2_index = ''
        for message in texts_by_language:
            message_2_index += "%s\n" % message.text
            message.update(indexed=True)
        try:
            os.makedirs('./messages')
        except OSError:
            pass
        with open('./messages/%s.txt' % language, 'w+') as messages_text:
            messages_text.write(message_2_index)
        return texts_by_language
