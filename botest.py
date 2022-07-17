import telebot
FILENAME = 'turetmap.txt'

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
        lng=float(line[0])
        value.append(lng)
        lan=float(line[1])
        value.append(lan)
        nome=str(line[2])
        value.append(nome)
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
    rmb=mindistanceturet(dati,lat_current,lng_current)
    lng_result=dati[rmb][0]
    lat_result=dati[rmb][1]
    name_result=dati[rmb][2]
    bot.send_location(message.chat.id,  lat_result , lng_result)
    bot.send_message(message.chat.id,"Ecco il toret piu' vicino :)")
    bot.send_message(message.chat.id,name_result)



def mindistanceturet(dati,lat_current,lng_current):
    minima_distanza=pow(pow(lat_current - dati[0][0], 2) + pow(lng_current - dati[0][1], 2), .5)
    countrmb=0
    for value in dati:
        distanza=pow(pow(lat_current - value[0], 2) + pow(lng_current - value[1], 2), .5)
        if(distanza<minima_distanza):
            minima_distanza=distanza
            rmb=countrmb
        countrmb=countrmb+1
    return rmb

bot.polling()
