#!/usr/bin/env python

import json
import logging
import requests
import traceback
import random
import copy

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, DESCRIPTIONS, ALIGNMENT_BUTTONS, CONFIRM, ATTRIBUTE_MENU
from pgcreation import (newpg, set_pg_name, class_picker, race_picker, attributes_picker, cancel_pg,
                        NAME, CLASS, RACE, ATTRIBUTES)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    custom_keyboard = [['/newpg', '/roll'],
                   ['/help','/listchar']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                 text="Welcome to an Interactive Character creation! Press /newpg to start",
                 reply_markup=reply_markup)

def help(update, context):
    update.message.reply_text('Command List:\n/help (Show this list)\n/me (User informations)\n/newpg \"PgName\" (Create new character)\n/roll \"Number\" (roll rando number from 1 to Number)')

def roll(update,context):
    if len(context.args)<1 :
        num= random.randint(1,20)
    else:
        num= random.randint(1,int(context.args[0]))
    update.message.reply_text(f"You rolled {num}")

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

def sheet(update,context):
    """Self informations"""
    pg=context.bot_data[update.effective_user['id']][context.args[0]]
    txt=f"This is a Character Sheet of {pg['name']}\n* an asterisk starts an unordered list\n* and this is another item in the list\n+ or you can also use the + character\n- or the - character\nTo start an ordered list, write this:\n\n1. this starts a list *with* numbers\n+  this will show as number \"2\"\n*  this will show as number \"3.\"\n9. any number, +, -, or * will keep the list going.\n   * just indent by 4 spaces (or tab) to make a sub-list\n     1. keep indenting for more sub lists\n  * here i'm back to the second level\nTo start a check list, write this:\n    - [ ] this is not checked\n    - [ ] this is too\n    - [x] but this is checked"
    context.bot.send_message(chat_id=update.message.chat_id, 
                            text=txt, 
                            parse_mode='Markdown')
                            
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
    dp.add_handler(CommandHandler("stop",stop))
    dp.add_handler(CommandHandler("sheet",sheet))
    dp.add_handler(CommandHandler("roll",roll))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("listchar", listchar))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newpg', newpg)],
        states={
            NAME: [MessageHandler(Filters.text, set_pg_name)],
            CLASS: [CallbackQueryHandler(class_picker)],
            RACE: [CallbackQueryHandler(race_picker)],
            ATTRIBUTES: [CallbackQueryHandler(attributes_picker)]
        },
        fallbacks=[CommandHandler('cancel', cancel_pg)]
    )
    dp.add_handler(conv_handler)

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
