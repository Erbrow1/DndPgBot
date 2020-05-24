# This is just a lot of long shit
from telegram import InlineKeyboardButton

CLASSES_BUTTONS = [[InlineKeyboardButton("Barbaro", callback_data='Barbaro'),
              InlineKeyboardButton("Bardo", callback_data='Bardo'),
              InlineKeyboardButton("Chierico", callback_data='Chierico'),
              InlineKeyboardButton("Druido", callback_data='Druido')],
              [InlineKeyboardButton("Guerriero", callback_data='Guerriero'),
              InlineKeyboardButton("Ladro", callback_data='Ladro'),
              InlineKeyboardButton("Mago", callback_data='Mago'),
              InlineKeyboardButton("Monaco", callback_data='Monaco')],
              [InlineKeyboardButton("Paladino", callback_data='Paladino'),
              InlineKeyboardButton("Ranger", callback_data='Ranger'),
              InlineKeyboardButton("Stregone", callback_data='Stregone'),
              InlineKeyboardButton("Warlock", callback_data='Warlock')]]
RACES_BUTTONS = [[InlineKeyboardButton("Umano", callback_data="Umano"),
        InlineKeyboardButton("Elfo", callback_data="Elfo"),
        InlineKeyboardButton("Nano", callback_data="Nano"),
        InlineKeyboardButton("Halfling", callback_data="Halfling")],
        [InlineKeyboardButton("Gnomo", callback_data="Gnomo"),
        InlineKeyboardButton("Tiefling", callback_data="Tiefling"),
        InlineKeyboardButton("Dragonborn", callback_data="Dragonborn")]]
