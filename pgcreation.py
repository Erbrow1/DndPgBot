import copy
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, DESCRIPTIONS, ALIGNMENT_BUTTONS, CONFIRM, ATTRIBUTE_MENU

NAME, CLASS, RACE, ALIGNMENT, ATTRIBUTES = range(5)

default_values = [ 15, 14, 13, 12, 10, 8 ]


class character(object):
    def __init__(self, name):
        self.name = name
        self.pgclass = None
        self.race = None
        self.background = None
        self.alignment = None
        self.attributes = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0
            }
        self.skills = {
            ""
            }
        self.proficiencies = []
        self.feats = []
        self.gear = []
        self.spells = []
        self.UNASSIGNED_ATTRS = [ "str", "dex",
                                  "con", "int",
                                  "wis", "cha" ]




pg_base = {
    "name": "",
    "class": "",
    "race": "",
    "alignment": "",
    "level": "",
    "attributes": {
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0,
        "extra": 0
        },
   
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

def newpg(update, context):
    """Starts the assisted character creation"""
    update.message.reply_text("How should your character be named?")
    context.user_data.update(copy.deepcopy(pg_base))
    return NAME

def set_pg_name(update, context):
    context.user_data["name"] = update.message.text
    reply_markup = InlineKeyboardMarkup(CLASSES_BUTTONS)
    context.bot.send_message(chat_id=update.effective_message.chat_id, text="Choose your class", reply_markup=reply_markup)
    return CLASS

def class_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["class"]])
        reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Choose your race", reply_markup=reply_markup)
        return RACE
    elif query.data == "Back":
        reply_markup = InlineKeyboardMarkup(CLASSES_BUTTONS)
        query.edit_message_text("Choose your class", reply_markup=reply_markup)
        return CLASS
    else:
        context.user_data["class"] = query.data
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS[query.data], reply_markup=reply_markup)
        return CLASS

def race_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["race"]])
        reply_markup = InlineKeyboardMarkup(ALIGNMENT_BUTTONS)
        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Choose your alignment", reply_markup=reply_markup)
        return ALIGNMENT
    elif query.data == "Back":
        reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
        query.edit_message_text("Choose your race", reply_markup=reply_markup)
        return RACE
    else:
        context.user_data["race"] = query.data
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS[query.data], reply_markup=reply_markup)
        return RACE

def alignment_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["alignment"]])
        reply_markup = InlineKeyboardMarkup(ATTRIBUTE_MENU(context.user_data["UNASSIGNED_ATTRS"]))
        txt = (f"Yadda yadda describe what attributes do\nYou still need to assign {context.user_data['ATTR_VALUES']}\n"
                f"Your attributes are:\nSTR: {context.user_data['attributes']['str']} | DEX: {context.user_data['attributes']['dex']} | CON: {context.user_data['attributes']['con']} | "
                f"INT: {context.user_data['attributes']['int']} | WIS: {context.user_data['attributes']['wis']} | CHA: {context.user_data['attributes']['cha']}\n"
                f"Which attribute should get a {context.user_data['ATTR_VALUES'][-1]}?")
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=txt, reply_markup=reply_markup)
        return ATTRIBUTES
    elif query.data == "Back":
        reply_markup = InlineKeyboardMarkup(ALIGNMENT_BUTTONS)
        query.edit_message_text("Choose your alignment", reply_markup=reply_markup)
        return ALIGNMENT
    else:
        context.user_data["alignment"] = query.data
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS[query.data], reply_markup=reply_markup)
        return ALIGNMENT

def attributes_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        # query.edit_message_text()
        query.edit_message_text(text=f"<b>STR</b> {context.user_data['attributes']['str']} | <b>DEX</b> {context.user_data['attributes']['dex']} | "
                                     f"<b>CON</b> {context.user_data['attributes']['con']} | <b>INT</b> {context.user_data['attributes']['int']} | "
                                     f"<b>WIS</b> {context.user_data['attributes']['wis']} | <b>CHA</b> {context.user_data['attributes']['cha']}", parse_mode="HTML")
        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Character created successfully!")
        uid = update.effective_user['id']
        if uid in context.bot_data:
            context.bot_data[uid][context.user_data['name']] = copy.deepcopy(context.user_data)
        else:
            context.bot_data[uid] = { context.user_data['name'] : copy.deepcopy(context.user_data) }
        context.user_data.clear()
        return ConversationHandler.END
    elif query.data == "Back":
        context.user_data["ATTR_VALUES"] = copy.deepcopy(pg_base["ATTR_VALUES"])
        context.user_data["UNASSIGNED_ATTRS"] = copy.deepcopy(pg_base["UNASSIGNED_ATTRS"])
    else:
        context.user_data["UNASSIGNED_ATTRS"].remove(query.data)
        context.user_data["attributes"][query.data] = context.user_data["ATTR_VALUES"][-1]
        context.user_data["ATTR_VALUES"] = context.user_data["ATTR_VALUES"][:-1]
    if context.user_data["UNASSIGNED_ATTRS"] == []:
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS["areyousure"], reply_markup=reply_markup)
        return ATTRIBUTES
    reply_markup = InlineKeyboardMarkup(ATTRIBUTE_MENU(context.user_data["UNASSIGNED_ATTRS"]))
    txt = (f"Yadda yadda describe what attributes do\nYou still need to assign {context.user_data['ATTR_VALUES']}\n"
            f"Your attributes are:\nSTR: {context.user_data['attributes']['str']} | DEX: {context.user_data['attributes']['dex']} | CON: {context.user_data['attributes']['con']} | "
            f"INT: {context.user_data['attributes']['int']} | WIS: {context.user_data['attributes']['wis']} | CHA: {context.user_data['attributes']['cha']}\n"
            f"Which attribute should get a {context.user_data['ATTR_VALUES'][-1]}?")
    query.edit_message_text(text=txt, reply_markup=reply_markup)
    return ATTRIBUTES


def cancel_pg(update, context):
    context.user_data.clear()
    update.message.reply_text("Character creation cancelled")
    return ConversationHandler.END
