from configs import *
from telebot import TeleBot
from telebot.types import Message
from bs4 import BeautifulSoup as bs
import requests
import urllib.parse
from reply import weather_btn
from telebot.types import ReplyKeyboardRemove


bot = TeleBot(TOKEN)

address = None


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    text = f'Привет {message.from_user.username}! Я бот для получения погоды. Чтобы узнать погоду нажмите на кнопку ниже'
    bot.send_message(chat_id, text, reply_markup=weather_btn())


@bot.message_handler(regexp='🌤🔍 Weather')
def reaction_to_btn(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Введите свой город английскими буквами', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, answer)
    global address
    address = True


@bot.message_handler(content_types=['text'])
def answer(message: Message):
    chat_id = message.chat.id
    global address
    if address:
        address = None
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Подождите...')
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(message.text) +'?format=json'
        response = requests.get(url).json()

        weather_url = f'https://weather.com/weather/today/l/{round(float(response[0]["lat"]), 2)},{round(float(response[0]["lon"]), 2)}?par=google'
        weather_response = requests.get(weather_url)

        html = bs(weather_response.content, 'html.parser')

        for el in html.select('.CurrentConditions--tempHiLoValue--3T1DG'):
            title = (int(el.select('span')[0].text.replace('°', '')) - 32)*5/9
        bot.send_message(chat_id, f'Макисмальная температура на сегодня: {round(title)}')
        i = 0
        for el in html.select('.CurrentConditions--tempHiLoValue--3T1DG'):
            title = (int(el.select('span:nth-of-type(2)')[0].text.replace('°', '')) - 32)*5/9

        bot.send_message(chat_id, f'Минимальная температура на сегодня : {round(title)}')

        bot.send_message(chat_id, 'Нажмите на кнопку чтобы узнать погоду где либо еще', reply_markup=weather_btn())



bot.polling(none_stop=True)