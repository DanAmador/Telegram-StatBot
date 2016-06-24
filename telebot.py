#!/usr/bin/env python3
import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dbHelper import dbHelper

db = dbHelper()


def learn(bot, update):
    # XXX: A lot of learning going on here
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
    stats = db.min_max_parse(update)
    bot.sendMessage(chat_id=update.message.chat_id, text=stats)


def initialize():
    logging.basicConfig(level=logging.DEBUG)
    with open('settings.json') as settings:
        token = json.load(settings).get("telegram_token")
        updater = Updater(token=token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('learn', learn))
    dispatcher.add_handler(CommandHandler('chatstats', count, pass_args=True))
    dispatcher.add_handler(CommandHandler('overall', overall))
    dispatcher.add_handler(MessageHandler([Filters.text], updates))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # XXX: Sure you want that in your debug log?
    logger.debug("shit's working, yo %s" % token)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    initialize()
