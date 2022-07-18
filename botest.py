import telebot
FILENAME = 'turetmap.txt'

API_TOKEN = '<Your token>'

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
    bot.reply_to(message,"""Se vi dicessimo che il simbolo di Torino non è la Mole Antonelliana, ma i toret? Cosa sono i "toret"? Ve lo sveliamo subito. 
    Si tratta delle tipiche fontanelle color verde bottiglia che come bocchettoni d’acqua hanno una testa di toro. Il torèt compare sempre più spesso nei negozi che promuovo i souvenir di Torino accanto ovviamente a quelli raffiguranti la Mole, il grande classico dei gadget.\
""")
    sendphoto(message)
    

@bot.message_handler(commands=['photo'])
def sendphoto(message):
    bot.send_photo(message.chat.id, 'https://i.pinimg.com/750x/f7/26/63/f726638483f45169631dcfa425261969.jpg')
    bot.reply_to(message, """\
Ciao, per favore mandami la tua posizione per trovare il toret più' vicino📍\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,"""Non riesco a capire, per favore mandami la tua posizione per trovare il toret più vicino📍\
""")
 
 #in questo modo mando la posizione tramite send_location e per ricavare le latitudini e longitudine utilizzo il campo 'location' e lat o lng ecc...
 #la parte importante è la prima riga in cui devo specificicare il content_types=["location"]
@bot.message_handler(content_types=["location"])
def location_received(message):
    print(message)
    bot.send_message(message.chat.id,"Posizione ricevuta")    
    searchnearturet(message.location.latitude, message.location.longitude,message)

@bot.message_handler(content_types=["location"])
def searchnearturet(lat_current,lng_current,message):
    dati=leggidati(FILENAME)
    rmb=mindistanceturet(dati,lat_current,lng_current)
    lng_result=dati[rmb][0]
    lat_result=dati[rmb][1]
    name_result=dati[rmb][2]
    bot.send_location(message.chat.id,  lat_result , lng_result)
    bot.send_message(message.chat.id,"Ecco il toret più vicino :)")
    bot.send_message(message.chat.id,name_result)

def mindistanceturet(dati,lat_current,lng_current):
    minima_distanza=pow(pow(lat_current - dati[0][1], 2) + pow(lng_current - dati[0][0], 2), .5)
    countrmb=0
    for value in dati:
        distanza=pow(pow(lat_current - value[1], 2) + pow(lng_current - value[0], 2), .5)
        if(distanza<minima_distanza):
            minima_distanza=distanza
            rmb=countrmb
        countrmb=countrmb+1
    return rmb

bot.polling()
