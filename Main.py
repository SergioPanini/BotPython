import sqlite3
DB_URL = r'db.sqlite3'

conn = sqlite3.connect(DB_URL)
cour = conn.cursor()

result = cour.execute("select * from main_table")
print("print1: ", result.fetchall())


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

result = cour.execute("select * from main_table")
print("print2: ", result.fetchall())


updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

Comand_up = ''

list_commands = '''
/write_name
/write_surname
/write_card
/write_phone

You can post me image and I sey number's car.
'''

def Start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, i am bot!" + list_commands)
Start_Handler = CommandHandler('start', Start)

#init bot interfase
def Write_name(update, context):
    global Comand_up 
    Comand_up = 'name'
    context.bot.send_message(chat_id=update.effective_chat.id, text='write name please')
    print(update.effective_chat.id)
Write_name_Handler = CommandHandler('write_name', Write_name)

def Write_surname(update, context):
    global Comand_up 
    Comand_up = 'surname'
    context.bot.send_message(chat_id=update.effective_chat.id, text='write surname please')
Write_surname_Handler = CommandHandler('write_surname', Write_surname)

def Write_phone_number(update, context):
    global Comand_up 
    Comand_up = 'phone'
    context.bot.send_message(chat_id=update.effective_chat.id, text='write phone  please')
Write_phone_Handler = CommandHandler('write_phone', Write_phone_number)

def Write_card(update, context):
    global Comands_up 
    Comand_up = 'card'
    context.bot.send_message(chat_id=update.effective_chat.id, text='write card please')
Write_card_Handler = CommandHandler('write_card', Write_card)

def Mess(update, context):
    global Comand_up
    
    result = cour.execute("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='tableName'")
    print(result.fetchall())
    
    #if cour.execute("SELECT * FROM main_table WHERE id = {0}".format(update.effective_chat.id)).fetchall():
    #    print('chat id found')
    #else: print('chat id not found')
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'You write:' + Comand_up)
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your car's number is :" + result_identification)


Get_Photo_Handler = MessageHandler(Filters.photo, Get_Photo)

dispatcher.add_handler(Start_Handler)
dispatcher.add_handler(Get_Photo_Handler)
dispatcher.add_handler(Write_name_Handler)
dispatcher.add_handler(Write_surname_Handler)
dispatcher.add_handler(Write_phone_Handler)
dispatcher.add_handler(Write_card_Handler)
dispatcher.add_handler(Mess_Handler)
updater.start_polling()