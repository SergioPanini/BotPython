from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
import os

Token = '506889620:AAEu2LhOhwYf0jcLLPnX2v3t0p38679198o'

updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

def Start(update, context):
    print('fffff')
Start_Handler = CommandHandler('start', Start)

def Get_Image(updater, context):
    print('i get img')
Get_Image_Handler = MessageHandler(Filters.document.category('image'), Get_Image)

def Get_Photo(bot, update):
    print('i get photo')
    print(update.message.photo[-1].file_id)
    print('work!!')

Get_Photo_Handler = MessageHandler(Filters.photo, Get_Photo)

dispatcher.add_handler(Start_Handler)
dispatcher.add_handler(Get_Image_Handler)
dispatcher.add_handler(Get_Photo_Handler)

updater.start_polling()