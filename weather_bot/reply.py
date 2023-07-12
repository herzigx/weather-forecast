from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def weather_btn():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='🌤🔍 Weather')
    murkup.add(btn)
    return murkup
