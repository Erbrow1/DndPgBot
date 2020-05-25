#!/usr/bin/env python

import json
import logging
import requests
import traceback
import random
import copy

from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, DESCRIPTIONS, ALIGNMENT_BUTTONS, CONFIRM, ATTRIBUTE_MENU

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

default_values = [ 15, 14, 13, 12, 10, 8 ]

pg_base = {
    "name": "",
    "class": "",
    "race": "",
    "alignment": "",
    "attributes": {
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0,
        "extra": 0
        },
    "level": 1,
    "experience": 0,
    "skills" : "LATER",
    "proficiencies": "LATER",
    "feats": "LATER",
    "spells": "OMGPLZNEVER",
    "gear": "Starting Gear",
    "background" : "Gay",
    "FIELDNUMBER": 0,
    "UNASSIGNED_ATTRS": ["str", "dex", "con", "int", "wis", "cha"],
    "ATTR_VALUES": [ 8, 10, 12, 13, 14, 15 ]
    }

FIELDS = [ "class", "race", "alignment", "attributes" ]

MENUS = {
    "confirm": CONFIRM,
    "class": CLASSES_BUTTONS,
    "race": RACES_BUTTONS,
    "alignment": ALIGNMENT_BUTTONS
    }



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    custom_keyboard = [['/makepg', '/roll'],
                   ['/help','/listchar']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                 text="Welcome to an Interactive Character creation! Press /makepg to start",
                 reply_markup=reply_markup)

def help(update, context):
    update.message.reply_text('Command List:\n/help (Show this list)\n/me (User informations)\n/makepg \"PgName\" (Create new character)\n/roll \"Number\" (roll rando number from 1 to Number)')

def roll(update,context):
    if len(context.args)<1 :
        num= random.randint(1,20)
    else:
        num= random.randint(1,int(context.args[0]))
    update.message.reply_text(f"You rolled {num}")

def display(query, context, field, value=None):
    if FIELDS[context.user_data["FIELDNUMBER"]] == "attributes" and field != "confirm":
        txt = (f"Yadda yadda describe what attributes do\nYou still need to assign {context.user_data['ATTR_VALUES']}\n"
                f"Your attributes are:\nSTR: {context.user_data['attributes']['str']} | DEX: {context.user_data['attributes']['dex']} | CON: {context.user_data['attributes']['con']} | "
                f"INT: {context.user_data['attributes']['int']} | WIS: {context.user_data['attributes']['wis']} | CHA: {context.user_data['attributes']['cha']}\n"
                f"Which attribute should get a {context.user_data['ATTR_VALUES'][-1]}?")
    elif value is None:
        txt = f"Choose your {field}"
    elif value in DESCRIPTIONS:
        txt = DESCRIPTIONS[value]
    else:
        txt = "TODO"
    if FIELDS[context.user_data["FIELDNUMBER"]] == "attributes" and field != "confirm":
        reply_markup = InlineKeyboardMarkup(ATTRIBUTE_MENU(context.user_data["UNASSIGNED_ATTRS"]))
    else:
        reply_markup = InlineKeyboardMarkup(MENUS[field])
    query.edit_message_text(text=txt, reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    uid = update.effective_user['id']
    query.answer()
    if context.user_data != {}:
        if query.data == "Confirm":
            context.user_data["FIELDNUMBER"] +=1
        elif query.data == "Back":
            if FIELDS[context.user_data["FIELDNUMBER"]] == "attributes":
                context.user_data["ATTR_VALUES"] = copy.deepcopy(pg_base["ATTR_VALUES"])
                context.user_data["UNASSIGNED_ATTRS"] = copy.deepcopy(pg_base["UNASSIGNED_ATTRS"])
            pass
        elif FIELDS[context.user_data["FIELDNUMBER"]] == "attributes":
            context.user_data["UNASSIGNED_ATTRS"].remove(query.data)
            context.user_data["attributes"][query.data] = context.user_data["ATTR_VALUES"][-1]
            context.user_data["ATTR_VALUES"] = context.user_data["ATTR_VALUES"][:-1]
            if context.user_data["UNASSIGNED_ATTRS"] == []:
                return display(query, context, "confirm", "areyousure")
        else:
            context.user_data[FIELDS[context.user_data["FIELDNUMBER"]]] = query.data
            return display(query, context, "confirm", query.data)
        if context.user_data["FIELDNUMBER"] >= len(FIELDS):
            query.edit_message_text(text="Character created")
            if uid in context.bot_data:
                context.bot_data[uid][context.user_data['name']] = copy.deepcopy(context.user_data)
            else:
                context.bot_data[uid] = { context.user_data['name'] : copy.deepcopy(context.user_data) }
            context.user_data.clear()
        else:
            display(query, context, FIELDS[context.user_data["FIELDNUMBER"]])

def makepg(update, context):
    """Makes a new pg"""
    if len(context.args) < 1:
        return update.message.reply_text('[!] You need to provide a character name')
    name = context.args[0]
    uid = update.effective_user['id']
    if context.user_data != {}:
        return update.message.reply_text('[!] You are already making a character!')
    context.user_data.update(copy.deepcopy(pg_base))
    context.user_data['name'] = name
    context.user_data['FIELDNUMBER'] = 0
    reply_markup = InlineKeyboardMarkup(CLASSES_BUTTONS)
    update.message.reply_text('Choose your class', reply_markup=reply_markup)

def listchar(update, context):
    # TODO print all fields
    text = ""
    if update.effective_user['id'] not in context.bot_data:
        return update.message.reply_text("[!] You have no characters")
    for char in context.bot_data[update.effective_user['id']].values():
        text += f"{char['name']} ({char['race']} {char['class']})\n"
    update.message.reply_text(text)

def stop(update, context):
    reply_markup = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text="Disabled buttons", reply_markup=reply_markup)

def me(update,context):
    """Self informations"""
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

    with open("chardb.json") as f:
        dp.bot_data.update(json.load(f))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("me",me))
    dp.add_handler(CommandHandler("makepg",makepg))
    dp.add_handler(CommandHandler("roll",roll))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("listchar", listchar))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("stop",stop))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    with open("chardb.json", "w") as f:
        json.dump(dp.bot_data, f)
    print("[x] Stopping bot")


if __name__ == '__main__':
    main()
