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
        "Dragonborn":   ("https://vignette.wikia.nocookie.net/forgottenrealms/images/3/3b/Dragonborn-5e.png/revision/latest?cb=20200308125107"
                        "Born of dragons, as their name proclaims, the dragonborn walk proudly through a world that greets them with fearful incomprehension."
                        "Shaped by draconic gods or the dragons themselves, dragonborn originally hatched from dragon eggs as a unique race, combining the best attributes of dragons and humanoids."),
        "Dwarf":        ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/254/420/618/636271781394265550.png"
                        "Most dwarves are lawful, believing firmly in the benefits of a well-ordered society."
                        " They tend toward good as well, with a strong sense of fair play and a belief that everyone deserves to share in the benefits of a just order."
                        " Size. Dwarves stand between 4 and 5 feet tall and average about 150 pounds."),
        "Elf":          ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/7/639/420/618/636287075350739045.png"
                        "Slender and Graceful\nWith their unearthly grace and fine features, elves appear hauntingly beautiful to humans and members of many other races."
                        " They are slightly shorter than humans on average, ranging from well under 5 feet tall to just over 6 feet. They are more slender than humans, weighing only 100 to 145 pounds."),
        "Gnome":        ("https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRowlh18XE_Zj-dBrIF7gKHPQ-MbFDZm6xn2rREDEO0M0kNnmrd&usqp=CAU"
                        "Gnomes are light-hearted, and even the tricksters amongst them favor harmless pranks over vicious schemes. Size."
                        " Gnomes are between 3 and 4 feet tall and weigh around 40 pounds. Your size is Small."),
        "Half-Elf":     ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/481/420/618/636274618102950794.png"
                        "Half-elves share the chaotic bent of their elven heritage. They both value personal freedom and creative expression, demonstrating neither love of leaders nor desire for followers."
                        " They chafe at rules, resent others' demands, and sometimes prove unreliable, or at least unpredictable."),
        "Halfling":     ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/256/420/618/636271789409776659.png"
                        "As a rule, they are good-hearted and kind, hate to see others in pain, and have no tolerance for oppression. They are also very orderly and traditional, leaning heavily on the support of their community and the comfort of the old ways."
                        " Size. Halflings average about 3 feet tall and weigh about 40 pounds."),
        "Half-Orc":     ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/466/420/618/636274570630462055.png"
                        "Half-Orcs raised among orcs and willing to live out their lives among them are usually evil. "
                        "Size: Half-Orcs are somewhat larger and bulkier than Humans, and they range from 5 to well over 6 feet tall. Your size is Medium. Speed: Your base walking speed is 30 feet."),
        "Human":        ("https://media-waterdeep.cursecdn.com/avatars/thumbnails/6/258/420/618/636271801914013762.png"
                        "Humans are the most adaptable and ambitious people among the common races. They have widely varying tastes, morals, and customs in the many different lands where they have settled."
                        " When they settle, though, they stay: they build cities to last for the ages, and great kingdoms that can persist for long centuries."),
        "Tiefling":     ("https://dndguide.com/wp-content/uploads/2018/04/Tiefling.png"
                        "Tiefling Traits\nTieflings share certain Racial Traits as a result of their Infernal descent. "
                        "Ability Score Increase: Your Intelligence score increases by 1, and your Charisma score increases by 2. Age: Tieflings mature at the same rate as Humans but live a few years longer."),
        "Lawful Good":  ("TODLawful Good. A lawful good character acts as a good person is expected or required to act. He combines a commitment to oppose evil with the discipline to fight relentlessly."
                        " He tells the truth, keeps his word, helps those in need, and speaks out against injustice.O"),
        "Neutral Good": ("A neutral good character does the best that a good person can do. He is devoted to helping others. He works with kings and magistrates but does not feel beholden to them."
                        " Neutral good is the best alignment you can be because it means doing what is good without bias for or against order."),
        "Chaotic Good": ("A chaotic good character acts as his conscience directs him with little regard for what others expect of him. He makes his own way, but he's kind and benevolent."
                        " He believes in goodness and right but has little use for laws and regulations. He hates it when people try to intimidate others and tell them what to do."),
        "Lawful Neutral":("Lawful neutral is the best alignment you can be because it means you are reliable and honorable without being a zealot."
                        " Lawful neutral can be a dangerous alignment when it seeks to eliminate all freedom, choice, and diversity in society. ..."
                        " Subordinates will be treated as is due their station within society."),
        "Neutral":      "Neutral is the best alignment you can be because it means you act naturally, without prejudice or compulsion. "
                        "Neutral can be a dangerous alignment when it represents apathy, indifference, and a lack of conviction",
        "Chaotic Neutral":("A chaotic neutral character follows his whims. He is an individualist first and last. "
                        "He values his own liberty but doesn't strive to protect others' freedom. He avoids authority, resents restrictions, and challenges traditions."),
        "Lawful Evil":("Lawful Evil. A lawful evil villain methodically takes what he wants within the limits of his code of conduct without regard for whom it hurts."
                        " He cares about tradition, loyalty, and order but not about freedom, dignity, or life. He plays by the rules but without mercy or compassion."),
        "Neutral Evil":("A neutral evil character is typically selfish and has no qualms about turning on allies-of-the-moment, and usually makes allies primarily to further their own goals. ... "
                        "Another valid interpretation of neutral evil holds up evil as an ideal, doing evil for evil's sake and trying to spread its influence."),
        "Chaotic Evil":("A chaotic evil character does whatever his greed, hatred, and lust for destruction drive him to do. He is hot-tempered, vicious, arbitrarily violent, and unpredictable. ..."
        " Chaotic evil beings believe their alignment is the best because it combines self-interest and pure freedom.")
    }

ALIGNMENT_BUTTONS = [[InlineKeyboardButton("Lawful Good", callback_data="Lawful Good"),
        InlineKeyboardButton("Neutral Good", callback_data="Neutral Good"),
        InlineKeyboardButton("Chaotic Good", callback_data="Chaotic Good")],
        [InlineKeyboardButton("Lawful Neutral", callback_data="Lawful Neutral"),
        InlineKeyboardButton("Neutral", callback_data="Neutral"),
        InlineKeyboardButton("Chaotic Neutral", callback_data="Chaotic Neutral")],
        [InlineKeyboardButton("Lawful Evil", callback_data="Lawful Evil"),
        InlineKeyboardButton("Neutral Evil", callback_data="Neutral Evil"),
        InlineKeyboardButton("Chaotic Evil", callback_data="Chaotic Evil")]]

def ATTRIBUTE_MENU(attr):
    ATTRIBUTE_BUTTONS = [[]]
    for val in attr:
        ATTRIBUTE_BUTTONS[0].append(InlineKeyboardButton(val, callback_data=val))
    return ATTRIBUTE_BUTTONS


class Race:
        SUB_RACE = {
                "Dwarf" : {
                "Hill Dwarf" : {
                        "con" : 2,
                        "wis" : 1
                        },
                "Mountai Dwarf":{
                        "str": 2,
                        "con": 2
                        }
                },
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
                },
                "Gnome":{
                        "Deep Gnome":{
                                "int" : 2,
                                "dex" : 1
                        },
                        "Rock Gnome":{
                                "int": 2,
                                "con":1
                        }
                },
                "Half-Elf":{
                        "Half-Elf":{
                                "cha" : 2,
                                "extra":2
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
                        "cha" : 0,
                        "extra": 0
                }

        def set_race(self, name, subrace):
                self.name = name
                self.subrace = subrace

                for att in self.SUB_RACE[name][subrace]:
                        self.attr_mod[att] += self.SUB_RACE[name][subrace][att]


LEVELS = {
        "1" :{
            "next_lvl" :300,
            "prof": 2
        },
        "2" :{
            "next_lvl" :900,
            "prof": 2
        },
        "3" :{
            "next_lvl" :2700,
            "prof": 2

        },
        "4" :{
            "next_lvl" :6500,
            "prof": 2
        },
        "5" :{
            "next_lvl" :14000,
            "prof": 3
        },
        "6" :{
            "next_lvl" :23000,
            "prof": 3
        },
        "7" :{
            "next_lvl" :34000,
            "prof": 3
        },
        "8" :{
            "next_lvl" :48000,
            "prof": 3
        },
        "9" :{
            "next_lvl" :64000,
            "prof": 4
        },
        "10":{
            "next_lvl" :85000,
            "prof": 4
        },
        "11":{
            "next_lvl" :100000,
            "prof": 4
        },
        "12":{
            "next_lvl" :120000,
            "prof": 4
        },
        "13":{
            "next_lvl" :140000,
            "prof": 5
        },
        "14":{
            "next_lvl" :165000,
            "prof": 5
        },
        "15":{
            "next_lvl" :195000,
            "prof": 5
        },
        "16":{
            "next_lvl" :225000,
            "prof": 5
        },
        "17":{
            "next_lvl" :26500,
            "prof": 6
        },
        "18":{
            "next_lvl" :30500,
            "prof": 6
        },
        "19":{
            "next_lvl" :355000,
            "prof": 6
        },
        "20":{
            "prof": 6
        }
    }
