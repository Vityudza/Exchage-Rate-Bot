import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot('1221914555:AAFQ4yhFyRWYFdU4-FQCo3SkGX9XOWI7LmI')

DOLLAR_UAH = 'https://www.google.com.ua/search?client=opera&q=долар+в+гривні&sourceid=opera&ie=UTF-8&oe=UTF-8'
EUR_UAH = 'https://www.google.com.ua/search?client=opera&hs=f3T&sxsrf=ALeKk03nhZV5Py-YdWsOUUqRCkIjDs9Vsw%3A1588002636620&ei=TP-mXvqvJa6rrgS5t5rgDw&q=євро+в+гривні&oq=євро+в+гривні&gs_lcp=CgZwc3ktYWIQAzIKCAAQxAIQRhCCAjICCAAyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIABBHOgQIABBDOgQIABAKOgkIIxAnEEYQggI6BQgAEMsBOgcIIxDqAhAnOgUIABCDAToJCAAQQxBGEIICOgcIABBGEIICUOHZvgFYy7O_AWDeub8BaAFwAngDgAF4iAHyEpIBBDIxLjWYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab&ved=0ahUKEwj6hbvo-ojpAhWulYsKHbmbBvwQ4dUDCAs&uact=5'
RUB_UAH = 'https://www.google.com.ua/search?client=opera&q=рублі+в+гривні&sourceid=opera&ie=UTF-8&oe=UTF-8'
DOLLAR_EUR = 'https://www.google.com.ua/search?client=opera&q=долар+в+євро&sourceid=opera&ie=UTF-8&oe=UTF-8'
EUR_DOLLAR = 'https://www.google.com.ua/search?client=opera&q=євро+в+долари&sourceid=opera&ie=UTF-8&oe=UTF-8'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137'
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row('Долар', '$->€')
    markup.row('Євро', '€->$')
    markup.row('Рублі')

    start_message = f'<b>Здоровенькі були {message.from_user.first_name}!</b><u>\n"Exchange Rate" - це бот, який переводить валюту у гривні</u>'
    help_message = f'<strong>ВАЖЛИВО!!!</strong>\n<i>Всього є три кнопки, кожна з яких показує поточний курс тої чи іншої валюти.\nОднак, у цьому боті також присутній калькулятор, який переводить <strong><u>ВВЕДЕНУ ВАМИ</u></strong> валюту у гривні, а також перевоидить долари в євро (кількість і через пробіл u_e) і євро в долари (кількість і через пробіл e_u). Наприклад "123 u_e"\n Для того, щоб перевести потрівно ввести кілкість цифрами і через пробіл валюту("usd" або "eur" або "rub").\nНаприкла "156 usd"</i>\n <b>Ви можете викликати це повідомлення ввівши команду /help</b>'

    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, help_message, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    help_message = f'<strong>ВАЖЛИВО!!!</strong>\n<i>Всього є три кнопки, кожна з яких показує поточний курс тої чи іншої валюти.\nОднак, у цьому боті також присутній калькулятор, який переводить <strong><u>ВВЕДЕНУ ВАМИ</u></strong> валюту у гривні, а також переводить долари в євро (кільсті і через пробіл u_e) і євро в долари (кількість і через пробіл e_u). Наприклад "123 e_u"\n Для того, щоб перевести потрівно ввести кілкість цифрами і через пробіл валюту("usd" або "eur" або "rub").\nНаприкла "156 usd"</i>'

    bot.send_message(message.chat.id, help_message, parse_mode='html')

def Rate(message, url, rate, name):
    full_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')

    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    final_message = f'<b>Курс:</b>\n<u>1 {rate} = {convert[0].text} {name}</u>'

    bot.send_message(message.chat.id, final_message,parse_mode='html')

def Calc(message, mess, url, rate, name):
    full_page = requests.get(url, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    count = convert[0].text.replace(',', '.')
    str_count = str(count)
    hrenovuy_result = float(str_count) * float(mess[0])
    result = round(hrenovuy_result, ndigits=2)

    final_message = f'<u>{mess[0]} {rate} = {result} {name}</u>'
    
    bot.send_message(message.chat.id, final_message, parse_mode='html')

@bot.message_handler(content_types=['text'])
def Main(message):
    get_message_from_user = message.text.strip().lower()
    base = get_message_from_user.split(' ')

    if base[0] == 'долар':
        Rate(message, DOLLAR_UAH, 'долар', 'гривень')
    elif base[0] == 'євро':
        Rate(message, EUR_UAH, 'євро', 'гривень')
    elif base[0] == 'рублі':
        Rate(message, RUB_UAH, 'російський рубль', 'гривень')
    elif base[0] == '$->€':
        Rate(message, DOLLAR_EUR, 'USD', 'євро')
    elif base[0] == '€->$':
        Rate(message, EUR_DOLLAR, 'EUR', 'доларів')
    elif base[0].isdigit() and base[1] == 'usd':
        print(type(base))
        Calc(message, base, DOLLAR_UAH, 'доларів', 'гривень')
    elif base[0].isdigit() and base[1] == 'eur':
        Calc(message, base, EUR_UAH, 'євро', 'гривень')
    elif base[0].isdigit() and base[1] == 'rub':
        Calc(message, base, RUB_UAH, ' рублів', 'гривень')
    elif base[0].isdigit() and base[1] == 'u_e':
        Calc(message, base, DOLLAR_EUR, 'доларів', 'євро')
    elif base[0].isdigit() and base[1] == 'e_u':
        Calc(message, base, EUR_DOLLAR, 'євро ', 'доларів')
    else:
        bot.send_message(message.chat.id, 'Дані введено не вірно скористайтеся командою <u>/help</u>', parse_mode='html')

bot.polling(none_stop=True)
