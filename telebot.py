#!/usr/bin/env python3

import json
import dbHelper

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


db = dbHelper()

def test(bot, update):
    bot.sendMessage()


def learn(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="aww yiss")


def updates(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def initialize():
    with open('settings.json') as settings:
        data = json.load(settings)
        updater = Updater(token=data["telegram_token"])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('learn', learn))
    dispatcher.add_handler(MessageHandler([Filters.text], updates))

    print("shit's working,yo %s") % data['telegram_token']
    updater.start_polling()


if __name__ == '__main__':
    initialize()