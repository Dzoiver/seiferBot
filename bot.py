from __future__ import print_function
import requests
import random
import telebot
import od_python
from telebot.types import Message
from od_python.rest import ApiException

# create an instance of the API class
api_instance = od_python.HeroesApi()
hero_id = 'hero_id_example' # str | Hero ID

opendotaOK = False

sleep_answers_yes = [
    'Да',
    'Ну конечно!',
    'Бегом в кровать!',
    'Естественно',
    'Самое время',
    'Да!'
]

sleep_answers_no = [
    'Нет',
    'Сон для слабаков!',
    'Нее',
    'Тебе решать',
    'Нет!',

]

privet_answers = [
    'привет',
    'ПРИВЕТ!',
    'Привет',
]
try:
    heroes = api_instance.heroes_get()

except ApiException as e:
    print("Exception when calling BenchmarksApi->benchmarks_get: %s\n" % e)
except:
    print('Connection reset error ')
else:
    opendotaOK = True

TOKEN = ''
tb = telebot.TeleBot(TOKEN)
# telebot.apihelper.proxy = {'http': 'http://62.210.38.159:8080'}
telebot.apihelper.proxy = {'http': 'http://199.21.99.15:80'}
telebot.apihelper.proxy = {'https': 'http://66.42.115.124:8080'}
telebot.apihelper.proxy = {'https': 'http://188.152.163.140:8118'}

command_list = ''' 
### Вот список моих команд ### 
# !привет - приветствует тебя
# !пойти спать - решает идти ли тебе спать
# !выбор - выбирает один из двух вариантов, разделённых словом "или". Формат: !выбор [вариант1] или [вариант2]
# !на ком сыграть - выбирает случайного героя из Dota 2
# !заметка - оставляет заметку о человеке. Формат: !заметка [имя] [информация]
### ###
'''


@tb.message_handler(commands=['start'])
def command_handler(message: Message):
    tb.reply_to(message, 'Я Seiferbot. Я говорю людям "привет" и помогаю людям определиться с выбором')

@tb.message_handler(commands=['help'])
def command_handler(message: Message):
    tb.reply_to(message, command_list)

@tb.message_handler(commands=['weather'])
def command_handler(message: Message):
    api_key = '4b4f27869ff5dd5617a6c5fd9f3b9870'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = 'ulyanovsk'
    current_temp = 0
    if len(message.text.split()) == 2:
        city = message.text[9:]
        url = base_url + "appid=" + api_key + "&q=" + city
        json_data = requests.get(url).json()
        info = json_data['main']
        current_temp = info['temp']
        tb.reply_to (message, 'Погода в городе ' + city + ' ' + str (int (current_temp) - 273) + ' градусов цельсия')
    if len(message.text.split()) > 2:
        city = message.text[9:message.text.find(' ')]
        url = base_url + "appid=" + api_key + "&q=" + city
        json_data = requests.get(url).json()
        info = json_data['main']
        current_temp = info['temp']
        tb.reply_to (message, 'Погода в городе ' + city + ' ' + str (int (current_temp) - 273) + ' градусов цельсия')
    if len(message.text.split()) == 1:
        tb.reply_to(message, 'Укажите город через пробел')



@tb.message_handler(content_types=['text'])
def echo_digits(message: Message):
    if '!ПОЙТИ СПАТЬ' in message.text.upper():
        respond = random.randint(0, 1)
        if respond == 1:
            tb.reply_to(message, sleep_answers_yes[random.randint(0, len(sleep_answers_yes) - 1)])
        else:
            tb.reply_to(message, sleep_answers_no[random.randint(0, len(sleep_answers_no) - 1)])
    if '!НА КОМ СЫГРАТЬ' in message.text.upper():
        try:
            if opendotaOK == True:
                tb.reply_to(message, str(heroes[random.randint(0, len(heroes) - 1)]._localized_name))
            else:
                tb.reply_to(message, 'Opendota не работает :(')
        except ApiException as e:
            tb.reply_to(message, 'Ой, opendota отвалилась')
            print('Opendota API error')
    if '!ПРИВЕТ' in message.text.upper():
        tb.reply_to(message, privet_answers[random.randint(0, len(privet_answers) - 1)])
    if '!ВЫБОР' in message.text.upper():
        index = message.text.find('или')
        if index == -1:
            tb.reply_to(message, 'Из чего выбирать?')
        else:
            index += 3
            if random.randint(0, 1) == 1:
                tb.reply_to(message, message.text[index:])
            else:
                tb.reply_to(message, message.text[6:index-4])
    if '!ЗАМЕТКА' in message.text.upper():
        if len(message.text.split()) > 2:
            substring = message.text[message.text.find(' ')+1:]
            spaceIndex2 = substring.find(' ')
            print(substring)
            name = substring[:spaceIndex2]
            note = substring[substring.find(' ')+1:]
            try:
                f = open(name + '.txt', 'a')
                f.write(note + '\n')
                f.close()
                f = open(name + '.txt', 'r')
                tb.reply_to(message, 'Заметки о ' + name +  ':\n' + f.read())
                f.close ()
            except FileNotFoundError:
                tb.reply_to(message, 'Ой, не могу найти файлик')
        if len(message.text.split()) == 2:
            name = message.text[message.text.find(' ')+1:]
            f = open(name + '.txt', 'r')
            tb.reply_to(message, f.read())

@tb.message_handler(content_types=['photo']) # Sends all images sent to bot to me
def saveImages(message: Message):
    fileinfo = tb.get_file(message.photo[0].file_id)
    tb.send_photo(396337180, fileinfo.file_id)

tb.polling(timeout=5)