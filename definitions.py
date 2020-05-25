# This is just a lot of long shit
from telegram import InlineKeyboardButton

CONFIRM = [[InlineKeyboardButton("Confirm", callback_data='Confirm'),
            InlineKeyboardButton("Back", callback_data='Back')]]

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

DESCRIPTIONS = {
        "areyousure":   "Do you want to confirm your attributes? Going back will start attribute assignment over",
        "Barbarian" :   ("https://i.pinimg.com/originals/d3/e1/4b/d3e14b7c318ff2ddb4fe25fda8757d4f.jpg\nTo a barbarian, though, "
                        "civilization is no virtue, but a sign of weakness. The strong embrace their animal nature—keen instincts, "
                        "primal physicality, and ferocious rage. ... Barbarians come alive in the chaos of combat.\n They can "
                        "enter a berserk state where rage takes over, giving them superhuman strength and resilience."),
        "Bard" :        ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/369/420/618/636272705936709430.png\n"
                        "The bard is a standard playable character class in many editions of the Dungeons & Dragons fantasy role-playing game."
                        " The bard class is versatile, capable of combat and of magic (divine magic in earlier editions, arcane magic in later editions)."
                        "Bards use their artistic talents to induce magical effects."),
        "Cleric" :      ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/371/420/618/636272706155064423.png\n"
                        "Clerics are versatile figures, both capable in combat and skilled in the use of divine magic (thaumaturgy)."
                        " Clerics are powerful healers due to the large number of healing and curative magics available to them. "
                        "With divinely-granted abilities over life or death, they are also able to repel or control undead creatures."),
        "Druid" :       ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/346/420/618/636272691461725405.png)\n"
                        "Whether calling on the elemental forces of nature or emulating the creatures of the animal world, druids are an embodiment of nature's resilience, cunning, and fury."
                        " They claim no mastery over nature, but see themselves as extensions of nature's indomitable will."),
        "Fighter" :     ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/359/420/618/636272697874197438.png\n"
                        "Fighters share an unparalleled mastery with weapons and armor, and a thorough knowledge of the skills of combat. "
                        "They are well acquainted with death, both meting it out and staring it defiantly in the face. You must have a Dexterity or Strength score of 13 or higher in order to multiclass in or out of this class."),
        "Monk":         ("https://www.seekpng.com/png/detail/107-1073422_monk-d-d-monk.png\n"
                        "Monks of the Way of the Open Hand are the ultimate masters of martial arts Combat, whether armed or unarmed."
                        "They learn Techniques to push and trip their opponents, manipulate ki to heal damage to their bodies, and practice advanced meditation that can protect them from harm."),
        "Paladin":      ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/365/420/618/636272701937419552.png\n"
                        "Oath of Devotion. The Oath of Devotion binds a paladin to the loftiest ideals of justice, virtue, and order."
                        "Sometimes called cavaliers, white knights, or holy warriors, these paladins meet the ideal of the knight in shining armor, acting with honor in pursuit of justice and the greater good."),
        "Ranger":       ("https://lootthebody.files.wordpress.com/2015/09/teagan_2.jpg?w=736\n"
                        "Far from the bustle of cities and towns, past the hedges that shelter the most distant farms from the terrors of the wild,"
                        " amid the dense-packed trees of trackless forests and across wide and empty plains, rangers keep their unending watch."),
        "Rogue":        ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/384/420/618/636272820319276620.png\n"
                        "Rogues rely on skill, stealth, and their foes' vulnerabilities to get the upper hand in any situation. They have a knack for finding the solution to just about any problem, demonstrating a resourcefulness and versatility that is the cornerstone of any successful adventuring party"),
        "Sorcerer":     ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/485/420/618/636274643818663058.png\n"
                        "Sorcerers carry a magical birthright conferred upon them by an exotic bloodline, some otherworldly influence, or exposure to unknown cosmic forces. No one chooses sorcery; the power chooses the sorcerer."
                        "You must have a Charisma score of 13 or higher in order to multiclass in or out of this class."),
        "Warlock":      ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/375/420/618/636272708661726603.png\n"
                        "Warlocks are seekers of the knowledge that lies hidden in the fabric of the multiverse. Through pacts made with mysterious beings of supernatural power, warlocks unlock magical effects both subtle and spectacular. You must have a Charisma score of 13 or higher in order to multiclass in or out of this class."),
        "Wizard":       ("https://vignette.wikia.nocookie.net/forgottenrealms/images/c/c0/Wizard_PHB5e.jpg/revision/latest?cb=20140921185413\n"
                        "Wizards are supreme magic-users, defined and united as a class by the spells they cast. Drawing on the subtle weave of magic that permeates the cosmos, wizards cast spells of explosive fire, arcing lightning, subtle deception, brute-force mind control, and much more."),
        "DragonBorn":   ("TODO"),
        "Dwarf":        ("TODO"),
        "Elf":          ("TODO"),
        "Gnome":        ("TODO"),
        "Half-Elf":     ("TODO"),
        "Half-Orc":     ("TODO"),
        "Human":        ("TODO"),
        "Tiefling":     ("TODO"),
        "Neutral":      "Literally wanted to play edgy evil character but party said NO"
    }

ALIGNMENT_BUTTONS = [[InlineKeyboardButton("Lawful Good", callback_data="Lawful Good"),
        InlineKeyboardButton("Neutral Good", callback_data="Neutral Good"),
        InlineKeyboardButton("Chaotic Good", callback_data="Chaotic Good")],
        [InlineKeyboardButton("Lawful Neutral", callback_data="Lawful Neutral"),
        InlineKeyboardButton("Neutral", callback_data="Neutral"),
        InlineKeyboardButton("Chaotic Neutral", callback_data="Chaotic Neutral")],
        [InlineKeyboardButton("Lawful Evil", callback_data="Lawful Evil"),
        InlineKeyboardButton("Neutral Evil", callback_data="Neutral Evil"),
        InlineKeyboardButton("Neutral Evil", callback_data="Neutral Evil")]]

def ATTRIBUTE_MENU(attr):
    ATTRIBUTE_BUTTONS = [[]]
    for val in attr:
        ATTRIBUTE_BUTTONS[0].append(InlineKeyboardButton(val, callback_data=val))
    return ATTRIBUTE_BUTTONS


class Race:
    SUB_RACE={
        "Dwarf" : {
            "Hill" : {
                "con" : 2,
                "wis" : 1
                },
            "Mountain":{
                "str": 2,
                "con": 2
                }
        "Elf" : {
            "Drow": {
                "dex": 2,
                "cha": 1,
                },
            "High Elf":{
                "dex": 2,
                "int": 1
                },
            "Wood Elf":{
                "dex" :2,
                "wis" :1
                }
            }
        }
        def __init__(self):
                self.name= "nome"
                self.subrace= "subrace"
                self.attr_mod = {
                        "str" : 0,
                        "dex" : 0,
                        "con" : 0,
                        "int" : 0,
                        "wis" : 0,
                        "cha" : 0
                }

        def set_race(self, name, subrace):
                self.name = name
                self.subrace = subrace
                for att in SUB_RACE[name][subrace]:
                        self.attr_mod[att] += SUB_RACE[name][subrace][att]

