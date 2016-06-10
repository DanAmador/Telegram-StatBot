#!/usr/bin/env python3
import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dbHelper import dbHelper


db = dbHelper()
def learn(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="aww yiss")


def updates(bot, update):
    db.messageInsert(update)


def count(bot, update,args):
    username,messages, words = db.count(update,args)
    results = "%s has sent  %s messages in this chat with a total of %s words" % (username,messages, words)
    bot.sendMessage(chat_id=update.message.chat_id, text=results)



def initialize():
    logging.basicConfig(level=logging.DEBUG)
    with open('settings.json') as settings:
        data = json.load(settings)
        updater = Updater(token=data["telegram_token"])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('learn', learn))
    dispatcher.add_handler(MessageHandler([Filters.text], updates))
    dispatcher.add_handler(CommandHandler('chatstats',count,pass_args=True))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug("shit's working,yo %s" % data['telegram_token'])

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    initialize()
