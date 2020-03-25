import telegram
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


users_data = {}

def Start(update, context):

    custom_keyboard_start = [['Регистрация', 'Ввести код парковки']]
    Start_text = '''
    Здравствуйте! Я ваш персональный помощник в поиске и оплате парковок.
    Для начала использования автоматизированных парковок вам требуется зарегистрировать
    свой аккаунт или ввести код парковки.
    '''

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start)
    context.bot.send_message(chat_id=update.effective_chat.id, text=Start_text, reply_markup=reply_markup)
    users_data[update.effective_chat.id] = {'Next_step': 'SelectRegOrNo'}

Start_Handler = CommandHandler('start', Start)

def SelectRegOrNo(update, context):
    if update.message.text == 'Регистрация':

        users_data[update.effective_chat.id]['Next_step'] = 'GetNameUser'
        context.bot.send_message(chat_id=update.effective_chat.id, text='введите имя плз')

    elif update.message.text == 'Ввести код парковки':

        context.bot.send_message(chat_id=update.effective_chat.id, text='Эту ветку нужно еще допилить')

    else: 
        custom_keyboard_start = [['Регистрация', 'Ввести код парковки']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Выберити пожалуйста один из вариантов', reply_markup=reply_markup)
  


def GetNameUser(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ветка регистрации')



def MessageGet(update, context):
    print('Get message!')
    list_models[users_data[update.effective_chat.id]['Next_step']](update, context)
    
MessageGet_Handler = MessageHandler(Filters.text, MessageGet)

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
dispatcher.add_handler(MessageGet_Handler)

list_models = {
                '/start': Start,
                'GetNameUser': GetNameUser,
                'SelectRegOrNo': SelectRegOrNo
             }

updater.start_polling()