import telebot

API_TOKEN = '5567408807:AAGamuBetRhvu2OHik91UmV5sK8AuOzrK9k'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Ciao, per favore mandami la tua posizione per trovarti il toret piu' vicino\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,"""Non posso capirlo, per favore mandami la tua posizione per trovarti il toret piu' vicino\
""")

bot.polling()
