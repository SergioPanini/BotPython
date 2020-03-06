from telegram.ext import Updater
from telegram.ext import CommandHandler


Token = '506889620:AAEu2LhOhwYf0jcLLPnX2v3t0p38679198o'

updater = Updater(Token=Token, use_context=True)
dispatcher = updater.dispatcher

def Start(update, context):
    print('fffff')
Start_Handler = CommandHandler('start', Start)


dispatcher.add_handler(Start_Handler)

update.start_pulling()