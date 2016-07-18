#!/usr/bin/env python3
import json
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dbHelper import Dbhelper

db = Dbhelper()


def languages_count():
    formatted_string = ""
    current_languages_count = Dbhelper.get_languages_message_count()
    for language, times in current_languages_count.iteritems():
        formatted_string += "\n%s:\t\t%d" % (language, times)
    return formatted_string


def index(bot, update, args):
    if len(args) is 0:
        from models import Texts
        available_languages = Texts.objects().only('language').distinct('language')
        for language in available_languages:
            db.index_messages_by_language(language, True)
    else:
        language_chosen = args[0]
        logging.info(args)

        db.index_messages_by_language(language_chosen)
        bot.sendMessage(chat_id=update.message.chat_id, text="Messages indexed")


def updates(bot, update):
    db.insert_message(update)


def count(bot, update, args):
    username, messages, words = db.count(update, args)

    sent_message = "%s has sent  %s messages in this chat with a total of %s words" if len(
            args) > 0 else "The chat %s has a total of %s messages with %s words"

    results = sent_message % (username, messages, words)
    bot.sendMessage(chat_id=update.message.chat_id, text=results)


def overall(bot, update):
    stats = db.parse_chat_stats(update)
    bot.sendMessage(chat_id=update.message.chat_id, text=stats)


def learn(bot, update,args):
    if len(args) > 1:
        bot.sendMessage(chat_id=update.message.chat_id, text="Forgot to add which language to learn")
    else:
        # TODO LEARN SUM SHIT
        pass





def initialize():
    logging.basicConfig(level=logging.DEBUG)
    with open('settings.json') as settings:
        token = json.load(settings).get("telegram_token")
        updater = Updater(token=token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('learn', learn, pass_args=True))
    dispatcher.add_handler(CommandHandler('index', index, pass_args=True))
    dispatcher.add_handler(CommandHandler('stats', count, pass_args=True))
    dispatcher.add_handler(CommandHandler('overall', overall))
    dispatcher.add_handler(MessageHandler([Filters.text], updates))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    initialize()
