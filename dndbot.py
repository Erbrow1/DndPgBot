#!/usr/bin/env python

import json
import logging
import requests
import traceback
import random

from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, ALIGNMENT_BUTTONS

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open("chardb.json") as f:
    CHARACTERS = json.load(f)

pg_base = {
    "name": "",
    "class": "",
    "race": "",
    "attributes": {
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0
        },
    "level": 1,
    "experience": 0,
    "skills" : "LATER",
    "NEXTFIELD" : "name",
    "DONE": False
    }

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    print(f"<@{update.effective_user['username']}> {update.message.text}")
    update.message.reply_text(f"Hey {update.effective_user['username']} \nWelcome to TESTANVEDICHEBOT!!\n Here you can create your DnD Characters. Enjoy it!!")

def help(update, context):
    update.message.reply_text('Command List:\n/help (Show this list)\n/me (User informations)\n/makepg \"PgName\" (Create new character)\n/roll \"Number\" (roll rando number from 1 to Number)')

def roll(update,context):
    if len(context.args)<1 :
        num= random.randint(1,20)
    else: 
        num= random.randint(1,int(context.args[0]))
    update.message.reply_text(f"You rolled {num}") 

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    uid = update.effective_user['id']
    if context.user_data != {}:
        context.user_data[context.user_data["NEXTFIELD"]] = query.data
        if context.user_data["NEXTFIELD"] == "class":
            reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
            context.user_data["NEXTFIELD"] = "race"
            query.edit_message_text(text="Choose your race", reply_markup=reply_markup)
        elif context.user_data["NEXTFIELD"] == "race":
            reply_markup = InlineKeyboardMarkup(ALIGNMENT_BUTTONS)
            context.user_data["NEXTFIELD"] = "alignment"
            query.edit_message_text(text="Choose your Alignment", reply_markup=reply_markup)
        elif context.user_data["NEXTFIELD"] == "alignment":
            context.user_data["DONE"] = True
            query.edit_message_text(text="Character created")
    if context.user_data["DONE"]:
        if uid in CHARACTERS:
            CHARACTERS[uid][context.user_data['name']] = context.user_data
        else:
            CHARACTERS[uid] = { context.user_data['name'] : context.user_data }
        with open("chardb.json", "w") as f:
            json.dump(CHARACTERS, f)
        context.user_data.clear()
    query.answer()

def makepg(update, context):
    """Makes a new pg"""
    if len(context.args) < 1:
        return update.message.reply_text('[!] You need to provide a character name')
    name = context.args[0]
    uid = update.effective_user['id']
    if context.user_data != {}:
        return update.message.reply_text('[!] You are already making a character!')
    context.user_data.update(pg_base)
    context.user_data['name'] = name
    context.user_data['NEXTFIELD'] = "class"
    reply_markup = InlineKeyboardMarkup(CLASSES_BUTTONS)
    update.message.reply_text('Choose your class', reply_markup=reply_markup)

def listchar(update, context):
    # TODO print all fields
    text = ""
    if update.effective_user['id'] not in CHARACTERS:
        return update.message.reply_text("[!] You have no characters")
    for char in CHARACTERS[update.effective_user['id']].values():
        print(char)
        # text += f"{char['name']} ({char['race']} {char['class']})\n"
    update.message.reply_text(text)

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
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    traceback.print_exc()

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
    dp.add_handler(CommandHandler("me",me))
    dp.add_handler(CommandHandler("makepg",makepg))
    dp.add_handler(CommandHandler("roll",roll))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("listchar", listchar))
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
