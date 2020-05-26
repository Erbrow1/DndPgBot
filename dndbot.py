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
    custom_keyboard = [['/sheet', '/newpg', '/roll'],
                   ['/help', '/delchar']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,
                 text="Welcome to an Interactive Character creation! Press /newpg to start",
                 reply_markup=reply_markup)

def help(update, context):
    update.message.reply_text("<b>Command List</b>\n"
                              "<u>/newpg</u> Create new character\n"
                              "<u>/sheet [pgname]</u> Show character sheet of <i>pgname</i> (or all characters if no name is given)\n"
                              "<u>/roll [number]</u> Roll randon integer from 1 to <i>number</i> (defaults 20)\n"
                              "<u>/delchar [pgname]</u> Delete character named <i>pgname</i>", parse_mode="HTML")

def roll(update,context):
    if len(context.args)<1 :
        num= random.randint(1,20)
    else:
        num= random.randint(1,int(context.args[0]))
    update.message.reply_text(f"You rolled <b><u>{num}</b></u>", parse_mode="HTML")

def stop(update, context):
    reply_markup = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, text="Disabled buttons", reply_markup=reply_markup)

def sheet(update,context):
    """Self informations"""
    if len(context.args) > 1 and context.args[0] in context.bot_data[update.effective_user['id']]:
        tgt_pgs = [ context.args[0] ]
    else:
        tgt_pgs = list(context.bot_data[update.effective_user['id']].keys())
    if tgt_pgs == []:
        return update.message.reply_text("You don't have any character")
    for pgname in tgt_pgs:
        pg = context.bot_data[update.effective_user['id']][pgname]
        txt = (f"<b>{pg['name']}</b> - {pg['alignment']}\n<u>{pg['race']} {pg['class']} (lvl {pg['level']})</u>\n\n<pre>STR  DEX  CON  INT  WIS  CHA \n"
              f" {pg['attributes']['str']:02d}   {pg['attributes']['dex']:02d}   {pg['attributes']['con']:02d}   "
              f"{pg['attributes']['int']:02d}   {pg['attributes']['wis']:02d}   {pg['attributes']['cha']:02d}\n\nSkills : TODO\n</pre>\n"
              f"Proficiencies : <s>{pg['proficiencies']}</s>\nFeats : <s>{pg['feats']}</s>\nGear : <s>{pg['gear']}</s>\n\nSpells : <s>{pg['spells']}</s>")
        context.bot.send_message(chat_id=update.message.chat_id, text=txt, parse_mode='HTML')

def delchar(update, context):
    if context.bot_data[update.effective_user['id']] == {}:
        update.message.reply_text("You don't have any character")
    elif len(context.args) < 1:
        char_buttons = []
        for pgname in context.bot_data[update.effective_user['id']]:
            char_buttons[0].append([InlineKeyboardButton(pgname, callback_data=pgname)])
        reply_markup = InlineKeyboardMarkup(char_buttons)
        hndl = CallbackQueryHandler(_delchar)
        context.dispatcher.add_handler(hndl, group=999)
        context.bot_data["delchar_handler"] = hndl
        update.effective_message.reply_text("Which character", reply_markup=reply_markup)
    else:
        fdb = context.bot_data[update.effective_user['id']].pop(context.args[0], None)
        if fdb is None:
            update.message.reply_text(f"No character named [{context.args[0]}]")
        else:
            update.message.reply_text(f"Successfully deleted [{context.args[0]}]")

def _delchar(update, context):
    query = update.callback_query
    context.bot_data[update.effective_user['id']].pop(query.data, None)
    query.edit_message_text(f"Successfully deleted [{query.data}]")
    context.dispatcher.remove_handler(context.bot_data["delchar_handler"], group=999)
    context.bot_data.pop("delchar_handler")

def error(update, context):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    traceback.print_exc()

def _logger(update, context):
    print(f"<@{update.effective_user['username']}> {update.message.text}")

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
        buf = json.load(f)
    dp.bot_data.clear()
    for k in buf:
        dp.bot_data[int(k)] = buf[k]
    # logger handler
    dp.add_handler(MessageHandler(Filters.text, _logger), group=123)
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop",stop))
    dp.add_handler(CommandHandler("sheet",sheet))
    dp.add_handler(CommandHandler("roll",roll))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("delchar", delchar))

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
