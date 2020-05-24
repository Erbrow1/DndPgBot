# This is just a lot of long shit
from telegram import InlineKeyboardButton

CONFIRM = [[InlineKeyboardButton("Confirm", callback_data='Confirm'),
            InlineKeyboardButton("Back", callback_data='Back')]]

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
        InlineKeyboardButton("Halfling", callback_data="Halfling"),
        InlineKeyboardButton("Gnomo", callback_data="Gnomo")],
        [InlineKeyboardButton("Mezzelfo", callback_data="Mezzelfo"),
        InlineKeyboardButton("Mezzorco", callback_data="Mezzorco"),
        InlineKeyboardButton("Tiefling", callback_data="Tiefling"),
        InlineKeyboardButton("Dragonborn", callback_data="Dragonborn")]]

ALIGNMENT_BUTTONS = [[InlineKeyboardButton("Legale Buono", callback_data="Legale Buono"),
        InlineKeyboardButton("Neutrale Buono", callback_data="Neutrale Buono"),
        InlineKeyboardButton("Caotico Buono", callback_data="Caotico Buono")],
        [InlineKeyboardButton("Legale Neutrale", callback_data="Legale Neutrale"),
        InlineKeyboardButton("Neutrale Puro", callback_data="Neutrale Puro"),
        InlineKeyboardButton("Caotico Neutrale", callback_data="Caotico Neutrale")],
        [InlineKeyboardButton("Legale Malvagio", callback_data="Legale Malvagio"),
        InlineKeyboardButton("Neutrale Malvagio", callback_data="Neutrale Malvagio"),
        InlineKeyboardButton("Caotico Malvagio", callback_data="Caotico Malvagio")]]
