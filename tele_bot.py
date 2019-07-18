import telebot
import base64


bot = telebot.TeleBot(base64.b64decode('NjQwODIzNzMzOkFBRlFhS0lGajJPMjZyT0VTaFQtbFJERUJlZzVodUY4ZUVj').decode('utf-8'))


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat_id, 'Ты написал мне /start, Бот запущен')


bot.polling()
