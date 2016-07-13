#!/usr/bin/env python3
import json
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dbHelper import dbHelper

db = dbHelper()


def languages_count():
    formatted_string = ""
    current_languages_count = dbHelper.get_current_languages()
    for language, times in current_languages_count.iteritems():
        formatted_string += "\n%s:\t\t%d" % (language, times)
    return formatted_string


def learn(bot, update, args):
    if len(args) is 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You forgot to add the language, the available languages are.. %s " % languages_count())
    else:
        #TODO update with DB dump depending on language chosen
        bot.sendMessage(chat_id=update.message.chat_id, text="aww yiss")


def updates(bot, update):
    db.insert_message(update)


def count(bot, update, args):
    username, messages, words = db.count(update, args)
    if args[0] is not 'all':
        sent_message = "%s has sent  %s messages in this chat with a total of %s words"
    else:
        sent_message = "The chat %s has a total of %s messages with %s words"

    results = sent_message % (username, messages, words)
    bot.sendMessage(chat_id=update.message.chat_id, text=results)


def overall(bot, update):
    stats = db.parse_chat_stats(update)
    bot.sendMessage(chat_id=update.message.chat_id, text=stats)


def initialize():
    logging.basicConfig(level=logging.DEBUG)
    with open('settings.json') as settings:
        token = json.load(settings).get("telegram_token")
        updater = Updater(token=token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('learn', learn, pass_args=True))
    dispatcher.add_handler(CommandHandler('chatstats', count, pass_args=True))
    dispatcher.add_handler(CommandHandler('overall', overall))
    dispatcher.add_handler(MessageHandler([Filters.text], updates))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    initialize()
