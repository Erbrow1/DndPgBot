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
    txt='<formclass="charsheet">\n<header>\n<sectionclass="charname">\n<labelfor="charname">CharacterName</label><inputname="charname"placeholder="ThoradinFireforge"/>\n</section>\n<sectionclass="misc">\n<ul>\n<li>\n<labelfor="classlevel">Class&Level</label><inputname="classlevel"placeholder="Paladin2"/>\n</li>\n<li>\n<labelfor="background">Background</label><inputname="background"placeholder="Acolyte"/>\n</li>\n<li>\n<labelfor="playername">PlayerName</label><inputname="playername"placeholder="PlayerMcPlayerface">\n</li>\n<li>\n<labelfor="race">Race</label><inputname="race"placeholder="Half-elf"/>\n</li>\n<li>\n<labelfor="alignment">Alignment</label><inputname="alignment"placeholder="LawfulGood"/>\n</li>\n<li>\n<labelfor="experiencepoints">ExperiencePoints</label><inputname="experiencepoints"placeholder="3240"/>\n</li>\n</ul>\n</section>\n</header>\n<main>\n<section>\n<sectionclass="attributes">\n<divclass="scores">\n<ul>\n<li>\n<divclass="score">\n<labelfor="Strengthscore">Strength</label><inputname="Strengthscore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Strengthmod"placeholder="+0"/>\n</div>\n</li>\n<li>\n<divclass="score">\n<labelfor="Dexterityscore">Dexterity</label><inputname="Dexterityscore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Dexteritymod"placeholder="+0"/>\n</div>\n</li>\n<li>\n<divclass="score">\n<labelfor="Constitutionscore">Constitution</label><inputname="Constitutionscore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Constitutionmod"placeholder="+0"/>\n</div>\n</li>\n<li>\n<divclass="score">\n<labelfor="Wisdomscore">Wisdom</label><inputname="Wisdomscore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Wisdommod"placeholder="+0"/>\n</div>\n</li>\n<li>\n<divclass="score">\n<labelfor="Intelligencescore">Intelligence</label><inputname="Intelligencescore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Intelligencemod"placeholder="+0"/>\n</div>\n</li>\n<li>\n<divclass="score">\n<labelfor="Charismascore">Charisma</label><inputname="Charismascore"placeholder="10"/>\n</div>\n<divclass="modifier">\n<inputname="Charismamod"placeholder="+0"/>\n</div>\n</li>\n</ul>\n</div>\n<divclass="attr-applications">\n<divclass="inspirationbox">\n<divclass="label-container">\n<labelfor="inspiration">Inspiration</label>\n</div>\n<inputname="inspiration"type="checkbox"/>\n</div>\n<divclass="proficiencybonusbox">\n<divclass="label-container">\n<labelfor="proficiencybonus">ProficiencyBonus</label>\n</div>\n<inputname="proficiencybonus"placeholder="+2"/>\n</div>\n<divclass="saveslist-sectionbox">\n<ul>\n<li>\n<labelfor="Strength-save">Strength</label><inputname="Strength-save"placeholder="+0"type="text"/><inputname="Strength-save-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Dexterity-save">Dexterity</label><inputname="Dexterity-save"placeholder="+0"type="text"/><inputname="Dexterity-save-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Constitution-save">Constitution</label><inputname="Constitution-save"placeholder="+0"type="text"/><inputname="Constitution-save-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Wisdom-save">Wisdom</label><inputname="Wisdom-save"placeholder="+0"type="text"/><inputname="Wisdom-save-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Intelligence-save">Intelligence</label><inputname="Intelligence-save"placeholder="+0"type="text"/><inputname="Intelligence-save-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Charisma-save">Charisma</label><inputname="Charisma-save"placeholder="+0"type="text"/><inputname="Charisma-save-prof"type="checkbox"/>\n</li>\n</ul>\n<divclass="label">\nSavingThrows\n</div>\n</div>\n<divclass="skillslist-sectionbox">\n<ul>\n<li>\n<labelfor="Acrobatics">Acrobatics<spanclass="skill">(Dex)</span></label><inputname="Acrobatics"placeholder="+0"type="text"/><inputname="Acrobatics-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="AnimalHandling">AnimalHandling<spanclass="skill">(Wis)</span></label><inputname="AnimalHandling"placeholder="+0"type="text"/><inputname="AnimalHandling-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Arcana">Arcana<spanclass="skill">(Int)</span></label><inputname="Arcana"placeholder="+0"type="text"/><inputname="Arcana-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Athletics">Athletics<spanclass="skill">(Str)</span></label><inputname="Athletics"placeholder="+0"type="text"/><inputname="Athletics-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Deception">Deception<spanclass="skill">(Cha)</span></label><inputname="Deception"placeholder="+0"type="text"/><inputname="Deception-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="History">History<spanclass="skill">(Int)</span></label><inputname="History"placeholder="+0"type="text"/><inputname="History-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Insight">Insight<spanclass="skill">(Wis)</span></label><inputname="Insight"placeholder="+0"type="text"/><inputname="Insight-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Intimidation">Intimidation<spanclass="skill">(Cha)</span></label><inputname="Intimidation"placeholder="+0"type="text"/><inputname="Intimidation-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Investigation">Investigation<spanclass="skill">(Int)</span></label><inputname="Investigation"placeholder="+0"type="text"/><inputname="Investigation-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Medicine">Medicine<spanclass="skill">(Wis)</span></label><inputname="Medicine"placeholder="+0"type="text"/><inputname="Medicine-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Nature">Nature<spanclass="skill">(Int)</span></label><inputname="Nature"placeholder="+0"type="text"/><inputname="Nature-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Perception">Perception<spanclass="skill">(Wis)</span></label><inputname="Perception"placeholder="+0"type="text"/><inputname="Perception-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Performance">Performance<spanclass="skill">(Cha)</span></label><inputname="Performance"placeholder="+0"type="text"/><inputname="Performance-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Persuasion">Persuasion<spanclass="skill">(Cha)</span></label><inputname="Persuasion"placeholder="+0"type="text"/><inputname="Persuasion-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Religion">Religion<spanclass="skill">(Int)</span></label><inputname="Religion"placeholder="+0"type="text"/><inputname="Religion-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="SleightofHand">SleightofHand<spanclass="skill">(Dex)</span></label><inputname="SleightofHand"placeholder="+0"type="text"/><inputname="SleightofHand-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Stealth">Stealth<spanclass="skill">(Dex)</span></label><inputname="Stealth"placeholder="+0"type="text"/><inputname="Stealth-prof"type="checkbox"/>\n</li>\n<li>\n<labelfor="Survival">Survival<spanclass="skill">(Wis)</span></label><inputname="Survival"placeholder="+0"type="text"/><inputname="Survival-prof"type="checkbox"/>\n</li>\n</ul>\n<divclass="label">\nSkills\n</div>\n</div>\n</div>\n</section>\n<divclass="passive-perceptionbox">\n<divclass="label-container">\n<labelfor="passiveperception">PassiveWisdom(Perception)</label>\n</div>\n<inputname="passiveperception"placeholder="10"/>\n</div>\n<divclass="otherprofsboxtextblock">\n<labelfor="otherprofs">OtherProficienciesandLanguages</label><textareaname="otherprofs"></textarea>\n</div>\n</section>\n<section>\n<sectionclass="combat">\n<divclass="armorclass">\n<div>\n<labelfor="ac">ArmorClass</label><inputname="ac"placeholder="10"type="text"/>\n</div>\n</div>\n<divclass="initiative">\n<div>\n<labelfor="initiative">Initiative</label><inputname="initiative"placeholder="+0"type="text"/>\n</div>\n</div>\n<divclass="speed">\n<div>\n<labelfor="speed">Speed</label><inputname="speed"placeholder="30"type="text"/>\n</div>\n</div>\n<divclass="hp">\n<divclass="regular">\n<divclass="max">\n<labelfor="maxhp">HitPointMaximum</label><inputname="maxhp"placeholder="10"type="text"/>\n</div>\n<divclass="current">\n<labelfor="currenthp">CurrentHitPoints</label><inputname="currenthp"type="text"/>\n</div>\n</div>\n<divclass="temporary">\n<labelfor="temphp">TemporaryHitPoints</label><inputname="temphp"type="text"/>\n</div>\n</div>\n<divclass="hitdice">\n<div>\n<divclass="total">\n<labelfor="totalhd">Total</label><inputname="totalhd"placeholder="2d10"type="text"/>\n</div>\n<divclass="remaining">\n<labelfor="remaininghd">HitDice</label><inputname="remaininghd"type="text"/>\n</div>\n</div>\n</div>\n<divclass="deathsaves">\n<div>\n<divclass="label">\n<label>DeathSaves</label>\n</div>\n<divclass="marks">\n<divclass="deathsuccesses">\n<label>Successes</label>\n<divclass="bubbles">\n<inputname="deathsuccess1"type="checkbox"/>\n<inputname="deathsuccess2"type="checkbox"/>\n<inputname="deathsuccess3"type="checkbox"/>\n</div>\n</div>\n<divclass="deathfails">\n<label>Failures</label>\n<divclass="bubbles">\n<inputname="deathfail1"type="checkbox"/>\n<inputname="deathfail2"type="checkbox"/>\n<inputname="deathfail3"type="checkbox"/>\n</div>\n</div>\n</div>\n</div>\n</div>\n</section>\n<sectionclass="attacksandspellcasting">\n<div>\n<label>Attacks&Spellcasting</label>\n<table>\n<thead>\n<tr>\n<th>\nName\n</th>\n<th>\nAtkBonus\n</th>\n<th>\nDamage/Type\n</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>\n<inputname="atkname1"type="text"/>\n</td>\n<td>\n<inputname="atkbonus1"type="text"/>\n</td>\n<td>\n<inputname="atkdamage1"type="text"/>\n</td>\n</tr>\n<tr>\n<td>\n<inputname="atkname2"type="text"/>\n</td>\n<td>\n<inputname="atkbonus2"type="text"/>\n</td>\n<td>\n<inputname="atkdamage2"type="text"/>\n</td>\n</tr>\n<tr>\n<td>\n<inputname="atkname3"type="text"/>\n</td>\n<td>\n<inputname="atkbonus3"type="text"/>\n</td>\n<td>\n<inputname="atkdamage3"type="text"/>\n</td>\n</tr>\n</tbody>\n</table>\n<textarea></textarea>\n</div>\n</section>\n<sectionclass="equipment">\n<div>\n<label>Equipment</label>\n<divclass="money">\n<ul>\n<li>\n<labelfor="cp">cp</label><inputname="cp"/>\n</li>\n<li>\n<labelfor="sp">sp</label><inputname="sp"/>\n</li>\n<li>\n<labelfor="ep">ep</label><inputname="ep"/>\n</li>\n<li>\n<labelfor="gp">gp</label><inputname="gp"/>\n</li>\n<li>\n<labelfor="pp">pp</label><inputname="pp"/>\n</li>\n</ul>\n</div>\n<textareaplaceholder="Equipmentlisthere"></textarea>\n</div>\n</section>\n</section>\n<section>\n<sectionclass="flavor">\n<divclass="personality">\n<labelfor="personality">Personality</label><textareaname="personality"></textarea>\n</div>\n<divclass="ideals">\n<labelfor="ideals">Ideals</label><textareaname="ideals"></textarea>\n</div>\n<divclass="bonds">\n<labelfor="bonds">Bonds</label><textareaname="bonds"></textarea>\n</div>\n<divclass="flaws">\n<labelfor="flaws">Flaws</label><textareaname="flaws"></textarea>\n</div>\n</section>\n<sectionclass="features">\n<div>\n<labelfor="features">Features&Traits</label><textareaname="features"></textarea>\n</div>\n</section>\n</section>\n</main>\n</form>'
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
        buf = json.load(f)
    dp.bot_data.clear()
    for k in buf:
        dp.bot_data[int(k)] = buf[k]
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
