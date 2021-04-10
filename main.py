from flask import Flask
from flask import request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
URL = 'https://api.telegram.org/bot1119459653:AAE7GyPDmCjT-pzLtGt_h9_VSivEwDzcZ0g'
sslify = SSLify(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        text = r['message']['text']
        data = {
            'login': text
        }
        r = requests.post('https://e-tashpmi.uz/bot/student_statistic/', data=data)
        if r.status_code == 201:
            send_document(chat_id, text)
        elif r.status_code == 404:
            send_message(chat_id, text='Такого ID  не существует ')
        elif r.status_code == 200:
            text = '''{}
    Курс {}
    ID  {}
    Оплаченная сумма {}
    Задолжность за первый семестер {}
    Задолжность за второй семестер {}
    Задолжность за учебный год {}
    ------------------------------
    Для полного ознакомления с предоставленными данными 
    можете обратиться в Маркетинг с 10:00 до 18:00 
    От понедельника до пятницы'''.format(r.json()['name'], r.json()['level'], r.json()['id_number'],
                                         r.json()['account']['overall_payment'],
                                         r.json()['account']['debt_for_first_semester'],
                                         r.json()['account']['debt_for_second_semester'],
                                         r.json()['account']['overall_debt'], )

            send_message(chat_id, text)
    return '<h1> Bot is running </h1>'


def send_message(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url=url, json=answer)
    return r.json()


def send_document(chat_id, text):
    url = URL + 'sendDocument'
    PATH = '/home/izzat/tashpmi/media/'
    with open(PATH + text + '.docx', 'rb') as doc:
        files = {"document": doc}
        title = '555.docx'
        r = requests.post(url=url, data={"chat_id": chat_id, "caption": title}, files=files)
        if r.status_code != 200:
            raise Exception("send error")
    return r.json()


if __name__ == '__main__':
    app.run()
