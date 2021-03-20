from pip._vendor import requests

from main import dp

from aiogram.types import Message


@dp.message_handler()
async def send_student_info(message: Message):
    r = requests.get('http://143.110.225.4/bot/student_list/' + message.text)
    if r.status_code == 404:
        await message.answer(text='Такого ID  не существует ')
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

        await message.answer(text=text)
