from __future__ import print_function
import requests
import random
import telebot
import od_python
from telebot.types import Message
from od_python.rest import ApiException
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import vk_api
import acc_data
from vk_api.tools import VkFunction

# print(photos.get('items'))

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
    'Здравствуй',
    'Добрый день',
    'Прифки',
    'Хай',
    'Приветик',
    'Здарова',
    'Хочу, чтобы животные могли разговаривать',

]

phrase_podderzhka = [
    'Выше нос! Давай попробуем изменить это печальное выражение на твоем лице. Когда ты улыбаешься, ты будто начинаешь светиться изнутри. Ради этого стоит придумать повод для улыбки',
    'У тебя уже были трудные моменты, которые остались позади. Согласись, что теперь уже многие из них забыты или вспоминаются смутно. Спустя какое-то время и эта неприятность останется размытым пятном в памяти',
    'Попробуй посмотреть на эту ситуацию с другой стороны. Ты обладаешь ценностями, столь желанными для многих: здоровьем, хорошей внешностью, живым умом и чувством юмора. С такими качествами нельзя долго унывать',
]
try:
    heroes = api_instance.heroes_get()

except ApiException as e:
    print("Exception when calling BenchmarksApi->benchmarks_get: %s\n" % e)
except:
    print('Connection reset error ')
else:
    opendotaOK = True


tb = telebot.TeleBot(acc_data.TOKEN)
# telebot.apihelper.proxy = {'http': 'http://62.210.38.159:8080'}
# telebot.apihelper.proxy = {'http': 'http://93.170.4.145:34148'}
# telebot.apihelper.proxy = {'http': 'http://180.247.5.10:8080'}
# telebot.apihelper.proxy = {'http': 'http://213.6.162.6:8080'}
# telebot.apihelper.proxy = {'http': 'http://178.150.84.139:38194'}
# telebot.apihelper.proxy = {'http': 'http://109.169.14.163:80'}
telebot.apihelper.proxy = {'https': 'http://186.103.175.158:3128'}
# telebot.apihelper.proxy = {'https': 'https://163.172.162.215:8811'}
# #
# telebot.apihelper.proxy = {'http': 'http://199.21.99.15:80'}
# telebot.apihelper.proxy = {'http': 'http://163.172.162.215:8811'}
# telebot.apihelper.proxy = {'https': 'http://183.89.177.65:8080'}
# telebot.apihelper.proxy = {'https': 'http://66.42.115.124:8080'}
# telebot.apihelper.proxy = {'https': 'http://188.152.163.140:8118'}

command_list = ''' 
### Вот список моих команд ### 
# !привет - приветствует тебя
# !пойти спать - решает идти ли тебе спать
# !выбор - выбирает один из двух вариантов, разделённых словом "или". Формат: !выбор [вариант1] или [вариант2]
# !на ком сыграть - выбирает случайного героя из Dota 2
# !заметка - оставляет заметку о человеке. Формат: !заметка [имя] [информация]
# !пикча - скидывает случайную картинку из альбома секретного пользователя вконтакте 
(не сработает, если у вас нет в друзьях этого пользователя)
# !мудрость - говорит вам случайную мудрую фразу
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
    if '!РОЛЛ' in message.text.upper():
        if len(message.text.split()) == 1:
            tb.reply_to(message, 'Напишите число через пробел')
        if len(message.text.split()) == 2:
            random_number = random.randint(0, int(message.text[message.text.find(' ')+1:]))
            tb.reply_to(message, str(random_number))
        if len(message.text.split()) > 2:
            substr = message.text[message.text.find(' '):]
            print(substr[1:])
            print(substr.find(' '))
            try:
                random_number = random.randint(0, int(substr[1:substr.find(' ')]))
                tb.reply_to(message, str(random_number))
            except:
                tb.reply_to(message, 'Пожалуйста только одно число после команды')

    if '!МУДРОСТЬ' in message.text.upper():
        my_url = 'https://randstuff.ru/saying/'
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, 'html.parser')
        saying = page_soup.find('div', {'id': 'saying'})
        sayingText = saying.table.tr.td.text
        tb.reply_to(message, sayingText)
    if '!ПИКЧА' in message.text.upper():
        vk_session = vk_api.VkApi(acc_data.vk_login, acc_data.vk_password)
        vk_session.auth()
        vk = vk_session.get_api()
        rnd = random.randint(0, 999)
        rndOffset = random.randint(0, 10416)
        photos = vk.photos.get(owner_id=364994731, album_id='saved', count=1000, offset=rndOffset)
        image = photos['items'][rnd]['sizes'][-1]['url']
        tb.reply_to(message, image)


@tb.message_handler(content_types=['photo']) # Sends all images sent to bot to me
def saveImages(message: Message):
    fileinfo = tb.get_file(message.photo[0].file_id)
    tb.send_photo(396337180, fileinfo.file_id)

@tb.message_handler(content_types=['sticker'])
def sendSticker(message: Message):
    pass
    # for e isn message.sticker
    # print(message.sticker)
    # tb.sticker
    # info = tb.get_sticker_set('Girls love story')

tb.polling(timeout=10)