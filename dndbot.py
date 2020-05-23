#!/usr/bin/env python

import json
import logging
import requests
import traceback
import random
import copy

from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, ALIGNMENT_BUTTONS, CONFIRM

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
        "cha": 0
        },
    "level": 1,
    "experience": 0,
    "skills" : "LATER",
    "FIELDNUMBER": 0,
    "NEXTFIELD" : "name",
    "DONE": False
    }

FIELDS = [ "class", "race", "alignment" ]

MENUS = {
    "confirm": CONFIRM,
    "class": CLASSES_BUTTONS,
    "race": RACES_BUTTONS,
    "alignment": ALIGNMENT_BUTTONS,
    "attributes": None
    }

DESCRIPTIONS = {
    "Barbarian": "https://i.pinimg.com/originals/d3/e1/4b/d3e14b7c318ff2ddb4fe25fda8757d4f.jpg\nBarbarian Class Details\nA tall human tribesman strides through a blizzard, draped in fur and hefting his axe. He laughs as he charges toward the frost giant who dared poach his people’s elk herd.\nA half-orc snarls at the latest challenger to her authority over their savage tribe, ready to break his neck with her bare hands as she did to the last six rivals.\nFrothigng at the mouth, a dwarf slams his helmet into the face of his drow foe, then turns to drive his armored elbow into the gut of another.\nThese barbarians, different as they might be, are defined by their rage: unbridled, unquenchable, and unthinking fury. More than a mere emotion, their anger is the ferocity of a cornered predator, the unrelenting assault of a storm, the churning turmoil of the sea.\nFor some, their rage springs from a communion with fierce animal spirits. Others draw from a roiling reservoir of anger at a world full of pain. For every barbarian, rage is a power that fuels not just a battle frenzy but also uncanny reflexes, resilience, and feats of strength.\nPrimal Instincti\nPeople of towns and cities take pride in how their civilized ways set them apart from animals, as if denying one’s own nature was a mark of superiority. To a barbarian, though, civilization is no virtue, but a sign of weakness. The strong embrace their animal nature—keen instincts, primal physicality, and ferocious rage. Barbarians are uncomfortable when hedged in by walls and crowds. They thrive in the wilds of their homelands: the tundra, jungle, or grasslands where their tribes live and hunt.\nBarbarians come alive in the chaos of combat. They can enter a berserk state where rage takes over, giving them superhuman strength and resilience. A barbarian can draw on this reservoir of fury only a few times without resting, but those few rages are usually sufficient to defeat whatever threats arise.\nA Life of Danger\nNot every member of the tribes deemed “barbarians” by scions of civilized society has the barbarian class. A true barbarian among these people is as uncommon as a skilled fighter in a town, and he or she plays a similar role as a protector of the people and a leader in times of war. Life in the wild places of the world is fraught with peril: rival tribes, deadly weather, and terrifying monsters. Barbarians charge headlong into that danger so that their people don’t have to.\nTheir courage in the face of danger makes barbarians perfectly suited for adventuring. Wandering is often a way of life for their native tribes, and the rootless life of the adventurer is little hardship for a barbarian. Some barbarians miss the close-knit family structures of the tribe, but eventually find them replaced by the bonds formed among the members of their adventuring parties.\nCreating a Barbarian\nWhen creating a barbarian character, think about where your character comes from and his or her place in the world. Talk with your DM about an appropriate origin for your barbarian. Did you come from a distant land, making you a stranger in the area of the campaign? Or is the campaign set in a rough-and-tumble frontier where barbarians are common?\nWhat led you to take up the adventuring life? Were you lured to settled lands by the promise of riches? Did you join forces with soldiers of those lands to face a shared threat? Did monsters or an invading horde drive you out of your homeland, making you a rootless refugee? Perhaps you were a prisoner of war, brought in chains to “civilized” lands and only now able to win your freedom. Or you might have been cast out from your people because of a crime you committed, a taboo you violated, or a coup that removed you from a position of authority.",
    "Wizard": "Skiidaadle Skidoodle your dick is now a noodle,hehehehe",
    "Neutral": "Literally wanted to play edgy evil character but party said NO"
    }

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f"Hey {update.effective_user['username']} \nWelcome to TESTANVEDICHEBOT!!\n Here you can create your DnD Characters. Enjoy it!!")

def help(update, context):
    update.message.reply_text('Command List:\n/help (Show this list)\n/me (User informations)\n/makepg \"PgName\" (Create new character)\n/roll \"Number\" (roll rando number from 1 to Number)')

def roll(update,context):
    if len(context.args)<1 :
        num= random.randint(1,20)
    else:
        num= random.randint(1,int(context.args[0]))
    update.message.reply_text(f"You rolled {num}")

def display(query, field, value=None):
    if value is None:
        txt = f"Choose your {field}"
    elif value in DESCRIPTIONS:
        txt = DESCRIPTIONS[value]
    else:
        txt = "TODO"
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
            pass
        else:
            context.user_data[FIELDS[context.user_data["FIELDNUMBER"]]] = query.data
            return display(query, "confirm", query.data)
        if context.user_data["FIELDNUMBER"] >= len(FIELDS):
            query.edit_message_text(text="Character created")
            if uid in context.bot_data:
                context.bot_data[uid][context.user_data['name']] = copy.deepcopy(context.user_data)
            else:
                context.bot_data[uid] = { context.user_data['name'] : copy.deepcopy(context.user_data) }
            context.user_data.clear()
        else:
            display(query, FIELDS[context.user_data["FIELDNUMBER"]])

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
    with open("chardb.json", "w") as f:
        json.dump(dp.bot_data, f)
    print("[x] Stopping bot")


if __name__ == '__main__':
    main()
