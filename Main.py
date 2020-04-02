import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
import logging

from BAPI import API
from Data import Token, SecretToken,  host

import base64
import json

import requests
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

A = API(host, SecretToken)

updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

#This dict save user data: steps, name and other
users_data = {}
#Messege if button no select
NOT_SELECT_BUTTON = 'Выберете один из пунктов'

TEXT_QUESTION_AND_ANSWER = '''
TEXT_QUESTION_AND_ANSWER
TEXT_QUESTION_AND_ANSWER
TEXT_QUESTION_AND_ANSWER

'''

with open('user_data.txt', 'r') as f:
        users_data = eval(f.read())

print('load data: ', users_data)


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
    if A.IsUser(update.effective_chat.id) == 'True':
        context.bot.send_message(chat_id=update.effective_chat.id, text='К сожелению ваш аккаунт уже есть в системе, обратитесь в тех поддержку.')
    else:
        custom_keyboard_start = [['Регистрация', 'Ввести код парковки']]
        Start_text = '''Здравствуйте! Я ваш персональный помощник в поиске и оплате парковок. \
Для начала использования автоматизированных парковок вам требуется зарегистрировать \
свой аккаунт или ввести код парковки.
        '''

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=Start_text, reply_markup=reply_markup)
        users_data[update.effective_chat.id] = {'Next_step': 'SelectRegOrNo'}

     

def SelectRegOrNo(update, context):
    if update.message.text == 'Регистрация':

        #custom_keyboard = [['one']]
        #reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        users_data[update.effective_chat.id]['Next_step'] = 'GetNameUser'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пожалуйста ваше имя')

    elif update.message.text == 'Ввести код парковки':
        custom_keyboard_start = [['Регистрация', 'Ввести код парковки']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Эту ветку нужно еще допилить', reply_markup=reply_markup)

    else: 
        custom_keyboard_start = [['Регистрация', 'Ввести код парковки']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Выберити пожалуйста один из вариантов', reply_markup=reply_markup)



def GetNameUser(update, context):
    users_data[update.effective_chat.id]['Name'] = update.message.text
    users_data[update.effective_chat.id]['Next_step'] = 'GetPhoneNumber'
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пожалуйста номер вашего телефона.')


def YesOrNoYouCarNumber(update, context):
    if update.message.text == 'Да':
        
        context.bot.send_message(chat_id=update.effective_chat.id, text='Как назовете этот автомобиль?')
        users_data[update.effective_chat.id]['Next_step'] = 'GetNameNumberAndPushMenu'

    elif update.message.text == 'Нет':

        users_data[update.effective_chat.id]['Next_step'] = 'GetUsersCarsNumber'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Какой номер у вашего автомобиля? Вы можете отправить мне фотографию номера или просто номер')

    else:
        custom_keyboard_start = [['Да', 'Нет']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Выберете, пожалуйста, один из вариантов ответа', reply_markup=reply_markup)


def GetUsersCarsNumber(update, context):
    print('GetUsersCarsNumber is calling')
    print(str(update.message.text))
    if update.message.text == None:
        Result = GetNumberOnPhote(update)
        if Result != False:
            
            custom_keyboard_start = [['Да', 'Нет']]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_start, one_time_keyboard=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля: ' + Result + ', все верно?', reply_markup=reply_markup)
            users_data[update.effective_chat.id]['CarNumber'] = Result
            users_data[update.effective_chat.id]['Next_step'] = 'YesOrNoYouCarNumber'
        
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Номер вашего автомобиля не распознан, отправьте фото еще раз или введите номер.')
            
    else:
        users_data[update.effective_chat.id]['CarNumber'] = update.message.text
        users_data[update.effective_chat.id]['Next_step'] = 'GetNameNumberAndPushMenu'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Как назовете этот автомобиль?')
    

def GetPhoneNumber(update, context):
    users_data[update.effective_chat.id]['Phone'] = update.message.text
    users_data[update.effective_chat.id]['Next_step'] = 'GetUsersCarsNumber'
    context.bot.send_message(chat_id=update.effective_chat.id, text='Какой номер у вашего автомобиля? Вы можете отправить мне фотографию номера или просто номер')

def GetNameNumberAndPushMenu(update, context):
    users_data[update.effective_chat.id]['NameNumber'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text='Отлично, все данные введены.')
    print('GetNameAndPushMenu, ', users_data)
    if A.AddUser(update.effective_chat.id, users_data[update.effective_chat.id]['Name'], 'None', users_data[update.effective_chat.id]['Phone']):
       print('User: {0} is adding'.format(update.effective_chat.id)) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Не удалось вас добавить в систему, обратитесь в техподдержку')
    
    if A.AddNumber(update.effective_chat.id, update.message.text, users_data[update.effective_chat.id]['CarNumber']):
       print('Number: {0} is adding'.format(users_data[update.effective_chat.id]['CarNumber'])) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Не удалось добавить номер  в систему, обратитесь в техподдержку')

    Menu(update, context)


def SelectMenu(update, context):
    if update.message.text == 'Текущий статус парковки':
        GetSatus(update, context)

    elif update.message.text == 'Оставить обращение в поддержку':
        custom_keyboard_toeditdata = [['Bернутся в меню']]
        text = '''
        Вы можете оставить нам сообщение и мы свяжемся с вами
        '''

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_toeditdata)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        users_data[update.effective_chat.id]['Next_step'] = 'GetMessageSupport'

    elif update.message.text == 'Вопросы и ответы':

        context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_QUESTION_AND_ANSWER)

    elif update.message.text == 'Изменить данные':
        custom_keyboard_toeditdata = [['Изменить ваше имя', 'Изменить телефон'], ['Изменить номер', 'Изменить имя автомобиля'], ['Вернутся в меню','']]
        text = '''
        Вы можете изменить следующие данные:
        -Ваше имя: {0}
        -Ваш номер телефона: {1}
        -Номер вашего автомобиля: {2}
        -Имя вашего автомобиля: {3}
        '''.format(users_data[update.effective_chat.id]['Name'], users_data[update.effective_chat.id]['Phone'], \
            users_data[update.effective_chat.id]['CarNumber'], users_data[update.effective_chat.id]['NameNumber'])

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_toeditdata)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
        users_data[update.effective_chat.id]['Next_step'] = 'SelectEditData'
    
    else: 
        Menu(update, context)

   


def GetMessageSupport(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ваше обращение зарегистрировано, с вами скоро свяжутся!')
    Menu(update, context)

def Menu(update, context):
    custom_keyboard_menu = [['Текущий статус парковки', 'Оставить обращение в поддержку'],['Вопросы и ответы', 'Изменить данные']]
    menu_text = '''
    Вам доступны следующий функции: Текущий статус парковки, Оставить обращение в поддержку, Вопросы и ответы, Изменить данные.
    '''

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_menu)
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text, reply_markup=reply_markup)
    users_data[update.effective_chat.id]['Next_step'] = 'SelectMenu'
    #print('menu, ', users_data)
    

def ToMenu(update, context):
    if update.message.text == 'Обновить статус':
        GetSatus(update, context)

    elif update.message.text == 'Вернутся в меню':
        Menu(update, context)

    else:
        custom_keyboard_tomenu = [['Обновить статус', 'Вернутся в меню']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_SELECT_BUTTON, reply_markup=reply_markup)
    

#This function get status parks use API
def GetSatus(update, context):
    custom_keyboard_tomenu = [['Обновить статус', 'Вернутся в меню']]
    res = A.GetStatus(update.effective_chat.id)
    print(res)

    if res == 'Parks is not':
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Машин на парковке нет', reply_markup=reply_markup)
        users_data[update.effective_chat.id]['Next_step'] = 'ToMenu'

    elif res != False:
        status_data = eval(res)
        if status_data['OUT'] == False:
            on_park = 'на парковке Parks&Me'
        else:
            on_park = 'не на парковке Parks&Me'
        status_text = '''
        Ваш автомобиль: {0}
        Номер автомобиля: {1}
        Статус: {2}
        Прошло времени: {3}
        Итого к оплате:
        '''.format(status_data['CarName'], status_data['CarNumber'], on_park, status_data['DeltaTime'].split('.')[0])

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=status_text, reply_markup=reply_markup)
        users_data[update.effective_chat.id]['Next_step'] = 'ToMenu'
    else:
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_tomenu)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Не удалось получить статус, обратитесь в тех. поддержку', reply_markup=reply_markup)
        
def SelectEditData(update, context):
    print(update.message.text)
    if update.message.text == 'Изменить ваше имя':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите новое имя ')
        users_data[update.effective_chat.id]['Next_step'] = 'EditName'

    elif update.message.text == 'Изменить телефон':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите новый телефон ')
        users_data[update.effective_chat.id]['Next_step'] = 'EditPhone'
        
    elif update.message.text == 'Изменить номер':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите новый номер ')
        users_data[update.effective_chat.id]['Next_step'] = 'EditCarNumber'

    elif update.message.text == 'Изменить имя автомобиля': 
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите новое имя автомобиля ')
        users_data[update.effective_chat.id]['Next_step'] = 'EditCarName'

    elif update.message.text == 'Вернутся в меню':
        Menu(update, context)
                
    else:
        custom_keyboard_toeditdata = [['Изменить ваше имя', 'Изменить телефон'], ['Изменить номер', 'Изменить номер автомобиля'], ['Вернутся в меню']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard_toeditdata)
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_SELECT_BUTTON, reply_markup=reply_markup)
    
def EditName(update, context):
    if A.EditName(update.effective_chat.id, update.message.text):
        users_data[update.effective_chat.id]['Name'] = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные обновлены')
        Menu(update, context)

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные не обновлены, обратитесь, пожалуйста, в тех. поддержку')
        Menu(update, context)

def EditPhone(update, context):
    if A.EditPhone(update.effective_chat.id, update.message.text):
        users_data[update.effective_chat.id]['Phone'] = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные обновлены')
        Menu(update, context)

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные не обновлены, обратитесь, пожалуйста, в тех. поддержку')
        Menu(update, context)

def EditCarNumber(update, context):
    if A.EditCarNumber(update.effective_chat.id, users_data[update.effective_chat.id]['CarNumber'], update.message.text):
        users_data[update.effective_chat.id]['CarNumber'] = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные обновлены')
        Menu(update, context)

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text='Данные не обновлены, обратитесь, пожалуйста, в тех. поддержку')
        Menu(update, context)

def EditCarName(update, context):
    print('edacarname')



def MessageGet(update, context):
    print('Get message! Chat:' + str(update.effective_chat.id))
    with open('user_data.txt', 'w') as f:
        f.write(str(users_data))
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
                'SelectEditData': SelectEditData,

                'EditName': EditName,
                'EditPhone': EditPhone,
                'EditCarNumber': EditCarNumber,
                'EditCarName': EditCarName,

                'GetMessageSupport': GetMessageSupport,
                'GetPhoneNumber': GetPhoneNumber,
                'YesOrNoYouCarNumber': YesOrNoYouCarNumber,
             }
print('________________Bot started__________________')


updater.start_polling()