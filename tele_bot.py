import telebot
import base64

token = base64.b64decode('NjQwODIzNzMzOkFBRlFhS0lGajJPMjZyT0VTaFQtbFJERUJlZzVodUY4ZUVj').decode('utf-8')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message, 'Ты написал мне /start, Бот запущен')


bot.polling()
