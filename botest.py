import telebot
FILENAME = 'touretmap.txt'

API_TOKEN = '5567408807:AAGamuBetRhvu2OHik91UmV5sK8AuOzrK9k'

bot = telebot.TeleBot(API_TOKEN)

def leggidati(file_name):
    dati = []
    try:
        turet_file = open(file_name, 'r')
    except:
        print("errore file ")
    next(turet_file) #salto la prima riga
    for line in turet_file:
        line=line.strip().split(",")
        value=[]
        nome=str(line[0])
        value.append(nome)
        id=int(line[1])
        value.append(id)
        lan=float(line[2])
        value.append(lan)
        lng=float(line[3])
        value.append(lng)
        dati.append(value)

    turet_file.close()
    return dati

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Ciao, per favore mandami la tua posizione per trovarti il toret piu' vicino📍\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,"""Non posso capirlo, per favore mandami la tua posizione per trovarti il toret piu' vicino📍\
""")
 
 #in questo modo mando la posizione tramite send_location e per ricavare le latitudini e longitudine utilizzo il campo 'location' e lat o lng ecc...
 #la parte importante è la prima riga in cui devo specificicare il content_types=["location"]
@bot.message_handler(content_types=["location"])
def location_received(message):
    print(message)
    bot.send_message(message.chat.id,"Località ricevuta")
    bot.send_message(message.chat.id,"Ricerca per il toret piu' vicino...")
    searchnearturet(message.location.latitude, message.location.longitude,message)

@bot.message_handler(content_types=["location"])
def searchnearturet(lat_current,lng_current,message):
    dati=leggidati(FILENAME)
    bot.send_location(message.chat.id,  lat_current , lng_current)
    bot.send_message(message.chat.id,"Ecco il toret piu' vicino :)")

bot.polling()
