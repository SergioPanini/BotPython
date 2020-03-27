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



updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

#This dict save user data: steps, name and other
users_data = {}

 #This functiions get photo and output car's number or false 
def GetNumberOnPhote(update):
    
    IMAGE_PATH = r'temp.jpeg'
    SECRET_KEY = r'sk_DEMODEMODEMODEMODEMODEMO'
    URL = r'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ru&secret_key=%s' % (SECRET_KEY)

    update.message.photo[-1].get_file().download(custom_path = 'temp.jpeg')

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    r = requests.post(URL, data = img_base64)
    s = json.dumps(r.json(), indent=3)
    try:
        result_identification = json.loads(s).get("results")[0].get('plate')
    except: 
        result_identification = False 
    
    print("Get new photo. Car's Number: ", result_identification)
    
    return result_identification

#start command
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
    users_data[update.effective_chat.id]['Name'] = update.message.text
    users_data[update.effective_chat.id]['Nex_step'] = 'GetUsersCarsNumber'
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пожалуйста номер вашегоавто в формате: O529TH197 или отправьте фото вашего номера.')


def GetUsersCarsNumber(update, context):
    print('GetUsersCarsNumber is calling')
    if update.message.text == '':
        Result = GetNumberOnPhote(update)
        if Result != False:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля: ' + Result)
            users_data[update.effective_chat.id]['Nex_step'] = 'GetNameNumber'
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля не распознан, отправьте фото еще раз или введите номер.')
    
    else:
        users_data[update.effective_chat.id]['CarNumber'] = update.message.text
        users_data[update.effective_chat.id]['Nex_step'] = 'GetNameNumber'
        
def GetNameNumber(update, context):
    print(users_data)








def MessageGet(update, context):
    print('Get message! Chat:' + str(update.effective_chat.id))
    list_models[users_data[update.effective_chat.id]['Next_step']](update, context)



#Init Handlers
Start_Handler = CommandHandler('start', Start)    
MessageGet_Handler = MessageHandler(Filters.text, MessageGet)
GetUsersCarsNumber_Handler = MessageHandler(Filters.photo, GetUsersCarsNumber)


dispatcher.add_handler(Start_Handler)
dispatcher.add_handler(GetUsersCarsNumber_Handler)
dispatcher.add_handler(MessageGet_Handler)


list_models = {
                '/start': Start,
                'GetNameUser': GetNameUser,
                'SelectRegOrNo': SelectRegOrNo,
                'GetUsersCarsNumber': GetUsersCarsNumber,
             }
print('________________Bot started__________________')


updater.start_polling()