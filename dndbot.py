#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license

import json
import logging
import requests

from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    update.message.reply_text('Benvenuto nel bot che per adesso fa solo vedere la lista delle classi disponibili')

def inline(update, context):
    keyboard = [[InlineKeyboardButton("Guerriero", callback_data='Guerriero'),
                 InlineKeyboardButton("Stregone", callback_data='Stregone')],
                [InlineKeyboardButton("Ranger", callback_data='Ranger')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    return query.data
    query.edit_message_text(text="Selected option: {}".format(query.data))

def makepg(update, context):
    """Makes a new pg"""
    name = context.args[0]
    pg = {
            "name": name,
            "class": "UNKNOWN",
            "gay": "100%"
    }
    pg[class]=inline(update,context)
    update.message,reply_text(f"You choose {pg[class]}")
    with open(f"{name}.json", "w") as f:
        json.dump(pg, f)
    update.message.reply_text(f"Made a new char named {name}")

def classes(update,context):
    """Gets list of classes"""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    message="Le classi sono :"
    with open("classes.txt") as fc:
        data = fc.read().split("\n")
    for elem in data:
        message= message+"\n"+elem

    update.message.reply_text(message)

def interactive(update, context):
    custom_keyboard = [['sei puttana', 'sei gay'],
                   ['sei op', 'sei ok']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                 text="Custom Keyboard Test",
                 reply_markup=reply_markup)

def stop_interactive(update, context):
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm back.", reply_markup=reply_markup)

def me(update,context):
    """Self informations"""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    user = update.effective_user
    update.message.reply_text(f"Benvenuto {user['username']}\nNome : {user['first_name']}\nCognome: {user['last_name']}\nID: {user['id']} ")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    print("[*] Starting bot")
    # Load config
    with open("config.json") as f:
        config = json.load(f)
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config["TOKEN"], use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("classes",classes))
    dp.add_handler(CommandHandler("me",me))
    dp.add_handler(CommandHandler("makepg",makepg))
    updater.dispatcher.add_handler(CommandHandler('inline', inline))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("interactive",interactive))
    dp.add_handler(CommandHandler("stop_interactive",stop_interactive))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    print("[x] Stopping bot")


if __name__ == '__main__':
    main()
