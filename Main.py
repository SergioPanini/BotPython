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

def Start(update, context):
    print('fffff')
Start_Handler = CommandHandler('start', Start)

def Get_Image(updater, context):
    print('i get img')
Get_Image_Handler = MessageHandler(Filters.document.category('image'), Get_Image)

def Get_Photo(update, context):
    print('i get photo')
    update.message.photo[-1].get_file().download(custom_path = 'temp.jpeg')
    os.system('ls')
    
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    r = requests.post(URL, data = img_base64)
    s = json.dumps(r.json(), indent=3)
    print(json.loads(s).get("results")[0].get('plate'))



Get_Photo_Handler = MessageHandler(Filters.photo, Get_Photo)

dispatcher.add_handler(Start_Handler)
dispatcher.add_handler(Get_Image_Handler)
dispatcher.add_handler(Get_Photo_Handler)

updater.start_polling()