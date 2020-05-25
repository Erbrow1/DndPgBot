import copy
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from definitions import CLASSES_BUTTONS, RACES_BUTTONS, DESCRIPTIONS, ALIGNMENT_BUTTONS, CONFIRM, ATTRIBUTE_MENU

NAME, CLASS, RACE, SUBRACE, ATTRIBUTES = range(4)

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

def newpg(update, context):
    """Starts the assisted character creation"""
    update.message.reply_text("How should your character be named?")
    context.user_data.update(copy.deepcopy(pg_base))
    return NAME

def set_pg_name(update, context):
    context.user_data["name"] = update.message.text
    reply_markup = InlineKeyboardMarkup(CLASSES_BUTTONS)
    update.effective_message.reply_text("Choose your class", reply_markup=reply_markup)
    return CLASS

def class_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["class"]])
        reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
        update.effective_message.reply_text("Choose your race", reply_markup=reply_markup)
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

def subrace_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["race"]])
        reply_markup = InlineKeyboardMarkup(ATTRIBUTE_MENU(context.user_data["UNASSIGNED_ATTRS"]))
        txt = (f"Yadda yadda describe what attributes do\nYou still need to assign {context.user_data['ATTR_VALUES']}\n"
                f"Your attributes are:\nSTR: {context.user_data['attributes']['str']} | DEX: {context.user_data['attributes']['dex']} | CON: {context.user_data['attributes']['con']} | "
                f"INT: {context.user_data['attributes']['int']} | WIS: {context.user_data['attributes']['wis']} | CHA: {context.user_data['attributes']['cha']}\n"
                f"Which attribute should get a {context.user_data['ATTR_VALUES'][-1]}?")
        update.effective_message.reply_text(txt, reply_markup=reply_markup)
        return ATTRIBUTES
    elif query.data == "Back":
        reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
        query.edit_message_text("Choose your race", reply_markup=reply_markup)
        return RACE
    else:
        context.user_data["race"] = query.data
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS[query.data], reply_markup=reply_markup)
        return RACE

def race_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        query.edit_message_text(text=DESCRIPTIONS[context.user_data["race"]])
        reply_markup = InlineKeyboardMarkup(ATTRIBUTE_MENU(context.user_data["UNASSIGNED_ATTRS"]))
        txt = (f"Yadda yadda describe what attributes do\nYou still need to assign {context.user_data['ATTR_VALUES']}\n"
                f"Your attributes are:\nSTR: {context.user_data['attributes']['str']} | DEX: {context.user_data['attributes']['dex']} | CON: {context.user_data['attributes']['con']} | "
                f"INT: {context.user_data['attributes']['int']} | WIS: {context.user_data['attributes']['wis']} | CHA: {context.user_data['attributes']['cha']}\n"
                f"Which attribute should get a {context.user_data['ATTR_VALUES'][-1]}?")
        update.effective_message.reply_text(txt, reply_markup=reply_markup)
        return ATTRIBUTES
    elif query.data == "Back":
        reply_markup = InlineKeyboardMarkup(RACES_BUTTONS)
        query.edit_message_text("Choose your race", reply_markup=reply_markup)
        return RACE
    else:
        context.user_data["race"] = query.data
        reply_markup = InlineKeyboardMarkup(CONFIRM)
        query.edit_message_text(text=DESCRIPTIONS[query.data], reply_markup=reply_markup)
        return RACE

def attributes_picker(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "Confirm":
        # query.edit_message_text()
        update.effective_message.reply_text("Character created successfully!")
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