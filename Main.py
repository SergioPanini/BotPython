from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
import logging

import requests
import base64
import json

import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

Token = '506889620:AAEu2LhOhwYf0jcLLPnX2v3t0p38679198o'

IMAGE_PATH = r'temp.jpeg'
SECRET_KEY = r'sk_DEMODEMODEMODEMODEMODEMO'
URL = r'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ru&secret_key=%s' % (SECRET_KEY)

updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

Comands_up = ''

list_commands = '''
/write_name
/write_surname
/write_card
/write_phone
'''

def Start(update, context):
    contex.bot.send_message(chat_id=update.effective_chat.id, text="Hi, i am bot!" + list_commands)
Start_Handler = CommandHandler('start', Start)

#init bot interfase
def Write_name(updater, context):
    Comands_up = 'write_name'
Write_name_Handler = CommandHandler('write_name', Write_name)

def Write_surname(updater, context):
    Comands_up = 'write_surname'
Write_surname_Handler = CommandHandler('write_surname', Write_surname)

def Write_phone_number(updater, context):
    Comands_up = 'write_phone'
Write_phone_Handler = CommandHandler('write_phone', Write_phone_number)

def Write_card(updater, context):
    Comands_up = 'write_card'
Write_card_Handler = CommandHandler('write_card', Write_card)

def Mess(update, context):
    print(Comands_up)
Mess_Handler = MessageHandler(Filters.text, Mess)


#identification number from photo
def Get_Photo(update, context):
    print('i get photo')
    update.message.photo[-1].get_file().download(custom_path = 'temp.jpeg')
    os.system('ls')
    
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    r = requests.post(URL, data = img_base64)
    s = json.dumps(r.json(), indent=3)
    result_identification = json.loads(s).get("results")[0].get('plate')
    print(result_identification)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Number car:" + result_identification)


Get_Photo_Handler = MessageHandler(Filters.photo, Get_Photo)

dispatcher.add_handler(Start_Handler)
dispatcher.add_handler(Get_Photo_Handler)
dispatcher.add_handler(Write_name_Handler)
dispatcher.add_handler(Write_surname_Handler)
dispatcher.add_handler(Write_phone_Handler)
dispatcher.add_handler(Write_card_Handler)
dispatcher.add_handler(Mess_Handler)
updater.start_polling()