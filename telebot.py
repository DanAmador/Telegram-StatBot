#!/usr/bin/env python3
import json
import logging
import subprocess

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dbHelper import Dbhelper
from min_char import min_char

db = Dbhelper()


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', './messages/%s.txt' % fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


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


def enlist_languages(language_map):
    languages = ''
    count = 0
    for value in sorted(language_map.items(), key=lambda x: x[1], reverse=True):
        if count < 10:
            languages += '%s: %s\n' % (value[0], value[1])
        count += 1
    return languages


def learn(bot, update, args):
    message = ''
    if len(args) < 1:
        message = "Forgot to add which language to learn \nAvailable languages with message total:\n%s" % enlist_languages(
                Dbhelper.get_languages_message_count())
    else:
        num_of_messages = file_len(args[0])
        try:
            if num_of_messages < 3000:
                raise ValueError
            ml_obj = min_char(args[0], args[1])
            message = ml_obj.learn()
        except ValueError:
            message = 'At least 3000 messages are needed, %s chat has %d messages.' % (args[0],num_of_messages)
        except IndexError:
            ml_obj = min_char(args[0], 5000)
            message = ml_obj.learn()
        except IOError:
            message = 'File for the language %s does not exist' % args[0]
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


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
