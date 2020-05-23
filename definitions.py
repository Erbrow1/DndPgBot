# This is just a lot of long shit
from telegram import InlineKeyboardButton

CLASSES_BUTTONS = [[InlineKeyboardButton("Barbarian", callback_data='Barbarian'),
              InlineKeyboardButton("Bard", callback_data='Bard'),
              InlineKeyboardButton("Cleric", callback_data='Cleric'),
              InlineKeyboardButton("Druid", callback_data='Druid')],
              [InlineKeyboardButton("Fighter", callback_data='Fighter'),
              InlineKeyboardButton("Monk", callback_data='Monk'),
              InlineKeyboardButton("Paladin", callback_data='Paladin'),
              InlineKeyboardButton("Ranger", callback_data='Ranger')],
              [InlineKeyboardButton("Rogue", callback_data='Rogue'),
              InlineKeyboardButton("Sorcerer", callback_data='Sorcerer'),
              InlineKeyboardButton("Warlock", callback_data='Warlock'),
              InlineKeyboardButton("Wizard", callback_data='Wizard')]]
RACES_BUTTONS = [[InlineKeyboardButton("Dragonborn", callback_data="Dragonborn"),
        InlineKeyboardButton("Dwarf", callback_data="Dwarf"),
        InlineKeyboardButton("Elf", callback_data="Elf"),
        InlineKeyboardButton("Gnome", callback_data="Gnome"),
        InlineKeyboardButton("Half-Elf", callback_data="Half-Elf")],
        [InlineKeyboardButton("Halfling", callback_data="Halfling"),
        InlineKeyboardButton("Half-Orc", callback_data="Half-Orc"),
        InlineKeyboardButton("Human", callback_data="Human"),
        InlineKeyboardButton("Tiefling", callback_data="Tiefling")]]

ALIGNMENT_BUTTONS = [[InlineKeyboardButton("Lawful Good", callback_data="Lawful Good"),
        InlineKeyboardButton("Neutral Good", callback_data="Neutral Good"),
        InlineKeyboardButton("Chaotic Good", callback_data="Chaotic Good")],
        [InlineKeyboardButton("Lawful Neutral", callback_data="Lawful Neutral"),
        InlineKeyboardButton("Neutral", callback_data="Neutral"),
        InlineKeyboardButton("Chaotic Neutral", callback_data="Chaotic Neutral")],
        [InlineKeyboardButton("Lawful Evil", callback_data="Lawful Evil"),
        InlineKeyboardButton("Neutral Evil", callback_data="Neutral Evil"),
        InlineKeyboardButton("Neutral Evil", callback_data="Neutral Evil")]]
