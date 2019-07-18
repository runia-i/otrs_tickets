import telebot
import base64


bot = telebot.TeleBot(base64.decode('NjQwODIzNzMzOkFBRlFhS0lGajJPMjZyT0VTaFQtbFJERUJlZzVodUY4ZUVj').decode('utf-8'))


@bot.message_handler(commands=['start'])
def start_bot(messenge):
    bot.send_message(messenge.chat_id, 'Ты написал мне /start, Бот запущен')


bot.polling()