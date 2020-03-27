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
#Messege if button no select
NOT_SELECT_BUTTON = 'Выберете один из пунктов'

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
    users_data[update.effective_chat.id]['Next_step'] = 'GetUsersCarsNumber'
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пожалуйста номер вашегоавто в формате: O529TH197 или отправьте фото вашего номера.')


def GetUsersCarsNumber(update, context):
    print('GetUsersCarsNumber is calling')
    print(str(update.message.text))
    if update.message.text == None:
        Result = GetNumberOnPhote(update)
        if Result != False:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля: ' + Result + 'Как назовете этот автомобиль?')
            users_data[update.effective_chat.id]['Next_step'] = 'GetNameNumberAndPushMenu'
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля не распознан, отправьте фото еще раз или введите номер.')
    
    else:
        users_data[update.effective_chat.id]['CarNumber'] = update.message.text
        users_data[update.effective_chat.id]['Next_step'] = 'GetNameNumberAndPushMenu'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Как назовете этот автомобиль?')
    
        
def GetNameNumberAndPushMenu(update, context):
    users_data[update.effective_chat.id]['Name'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text='Отлично, все данные введены.')

    custom_keyboard_menu = [['Текущий статус парковки', 'Оставить обращение в поддержку'],['Вопросы и ответы', 'Изменить данные']]
    menu_text = '''
    Вам доступны следующий функции: Текущий статус парковки,
    Оставить обращение в поддержку, Вопросы и ответы, Изменить данные.
    '''

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_menu)
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text, reply_markup=reply_markup)
    users_data[update.effective_chat.id]['Next_step'] = 'SelectMenu'


def SelectMenu(update, context):
    if update.message.text == 'Текущий статус парковки':
        GetSatus(update, context)

    elif update.message.text == 'Оставить обращение в поддержку':

        context.bot.send_message(chat_id=update.effective_chat.id, text='Эту ветку нужно еще допилить')

    elif update.message.text == 'Вопросы и ответы':

        context.bot.send_message(chat_id=update.effective_chat.id, text='Эту ветку нужно еще допилить')

    elif update.message.text == 'Изменить данные':
        custom_keyboard_toeditdata = [['изменить имя', 'изменить телефон'], ['изменить номер', 'изменить ник'], ['вернутся в меню']]
        text = '''
        Вы можете изменить следующие данные:
        -Ваше имя: @name
        -Ваш номер телефона: @phone
        -Номер вашего автомобиля: @carnumber
        '''
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    else: 
        custom_keyboard_menu = [['Текущий статус парковки', 'Оставить обращение в поддержку'],['Вопросы и ответы', 'Изменить данные']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_menu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_SELECT_BUTTON, reply_markup=reply_markup)

def ToMenu(update, context):
    if update.message.text == 'Обновить статус':
        GetSatus(update, context)

    elif update.message.text == 'Вернутся в меню':
        custom_keyboard_menu = [['Текущий статус парковки', 'Оставить обращение в поддержку'],['Вопросы и ответы', 'Изменить данные']]
        menu_text = '''
        Вам доступны следующий функции: Текущий статус парковки,
        Оставить обращение в поддержку, Вопросы и ответы, Изменить данные.
        '''

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_menu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text, reply_markup=reply_markup)
        users_data[update.effective_chat.id]['Next_step'] = 'SelectMenu'
    
    else:
        custom_keyboard_tomenu = [['Обновить статус', 'Вернутся в меню']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_SELECT_BUTTON, reply_markup=reply_markup)
    

#This function get status parks use API
def GetSatus(update, context):
    custom_keyboard_tomenu = [['Обновить статус', 'Вернутся в меню']]
    status_text = '''
    Ваш автомобиль $Ник автомобиля:
    Номер автомобиля: $car number
    Статус: не на парковке Parks&Me / на парковке Parks&Me
    Прошло времени: $time
    Итого к оплате:
    '''

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
    context.bot.send_message(chat_id=update.effective_chat.id, text=status_text, reply_markup=reply_markup)
    users_data[update.effective_chat.id]['Next_step'] = 'ToMenu'

def SelectEditData(update, context):
    if update.message.text == 'изменить имя':
        GetSatus(update, context)

    elif update.message.text == 'изменить телефон':
        pass
    elif update.message.text == 'изменить номер':
        pass
    elif update.message.text == 'изменить ник': 
        pass
    elif update.message.text == 'вернутся в меню':

    else:
        custom_keyboard_tomenu = [['Обновить статус', 'Вернутся в меню']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_SELECT_BUTTON, reply_markup=reply_markup)
    
def EditName(update, context):
    pass

def EditPhone(update, context):
    pass

def EditCarNumber(update, context):
    pass



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
                'GetNameNumberAndPushMenu': GetNameNumberAndPushMenu,
                'SelectMenu': SelectMenu,
                'GetSatus': GetSatus,
                'ToMenu': ToMenu,
             }
print('________________Bot started__________________')


updater.start_polling()