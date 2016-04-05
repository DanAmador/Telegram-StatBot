import json

from telegram.ext import *

with open('settings.json') as settings:
    data = json.load(settings)
    updater = Updater(data["telegram_token"])


def test(bot, update):
    bot.sendMessage()
