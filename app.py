import requests.exceptions
import telebot
from config import TOKEN, currencies
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video',
                                    'video_note', 'voice', 'location', 'contact'])
def help(message: telebot.types.Message):
    text = 'К сожалению, я умею обрабатывать только текстовые команды'
    bot.reply_to(message, text)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<количество переводимой валюты>\n' \
           'ПРИМЕР: доллар рубль 100\n' \
           'Посмотреть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        key = '- ' + key
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        input_data = message.text.split()

        if len(input_data) > 3:
            raise APIException('Слишком много параметров')
        elif len(input_data) < 3:
            raise APIException('Слишком мало параметров')

        base, quote, amount = input_data
        result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    except requests.exceptions.ReadTimeout as e:
        bot.send_message(message.chat.id, f'Потерял связь\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {result}'
        bot.reply_to(message, text)


if '__main__' == __name__:
    bot.polling()
