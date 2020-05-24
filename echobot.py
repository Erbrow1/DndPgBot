#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license

import json
import logging
import requests

from uuid import uuid4
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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


def help(update, context):
    """Send a message when the command /help is issued."""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    update.message.reply_text(update.message.text)

def fact(update, context):
    """Gets a random fact"""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json", timeout=5)
        data = r.json()
        update.message.reply_text(f"{data['text']} ({data['source']})")
    except:
        update.message.reply_text("Could not fetch a random fact")

def classes(update,context):
    """Gets list of classes"""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    message="Le classi sono :"
    with open("classes.txt") as fc:
        data = fc.read().split("\n")
    for elem in data:
        message= message+"\n"+elem

    update.message.reply_text(message)

def me(update,context):
    """Self informations"""
   # user= link()
    print(f"<update.effective_user['username']> {update.message.text}")
    update.message.reply_text("Benvenuto"+ user['username']+" \nNome :"+ user['first_name'] +"\nCognome: "+user['last_name'])


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
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("fact", fact))
    dp.add_handler(CommandHandler("classes",classes))
    dp.add_handler(CommandHandler("me",me))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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
