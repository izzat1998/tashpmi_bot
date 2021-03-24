from os import listdir
from os.path import isfile, join

from pip._vendor import requests
import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствует бот университета ТашПМИ')


@bot.message_handler(content_types=['text'])
def send_text(message):
    PATH = '/home/izzat/tashpmi/media/'
    file_names = [f for f in listdir(PATH) if
                  isfile(join(PATH, f))]

    if message.text == '103103':
        data = {
            'directions': ['Даволаш иши', 'Тиббий педагогика'],
            'levels': [6, 6],
            'login': message.text
        }
        requests.post('http://143.110.225.4/bot/student_statistic/', data=data)

        doc = open(PATH + message.text + '.docx', 'rb')
        bot.send_document(message.chat.id, doc)
    else:
        r = requests.get('http://143.110.225.4/bot/student_list/' + message.text)
        if r.status_code == 404:
            bot.send_message(chat_id=message.chat.id, text='Такого ID  не существует ')
        elif r.status_code == 200:
            text = '''{}
Курс {}
ID  {}
Оплачено {}
Задолжность за первый семестер {}
Задолжность за второй семестер {}
Задолжность за учебный год {}'''.format(r.json()['name'], r.json()['level'], r.json()['id_number'],
                                        r.json()['account']['overall_payment'],
                                        r.json()['account']['debt_for_first_semester'],
                                        r.json()['account']['debt_for_second_semester'],
                                        r.json()['account']['overall_debt'], )

        bot.send_message(message.chat.id, text=text)


bot.polling()
