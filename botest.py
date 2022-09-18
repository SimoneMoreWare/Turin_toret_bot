import telebot
from telebot import types
from urllib.request import urlopen
import requests
import json

FILENAME = ""
API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

def leggidati(file_name):
    
    dati = []

    try:
        turet_file = json.loads(requests.get(FILENAME).text)
    except:
        print("errore file json")

    dim=len(turet_file)
    for i in range(dim):
        value=[]
        lng=float(turet_file[i]['latlng']['longitude'])
        value.append(lng)
        lan=float(turet_file[i]['latlng']['latitude'])
        value.append(lan)
        nome=str(turet_file[i]['address'])
        value.append(nome)
        dati.append(value)

    return dati

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Manda La tua posizione', request_location=True)
    markup.add(itembtn1)
    bot.send_message(message.chat.id, """Se vi dicessimo che il simbolo di Torino non è la Mole Antonelliana, ma i toret? Cosa sono i "toret"? Ve lo sveliamo subito. 
    Si tratta delle tipiche fontanelle color verde bottiglia che come bocchettoni d’acqua hanno una testa di toro. Il torèt compare sempre più spesso nei negozi che promuovo i souvenir di Torino accanto ovviamente a quelli raffiguranti la Mole, il grande classico dei gadget.\
""" ,reply_markup=markup)
    bot.send_photo(message.chat.id, 'https://i.pinimg.com/750x/f7/26/63/f726638483f45169631dcfa425261969.jpg')
    bot.reply_to(message, """\
Ciao, per favore mandami la tua posizione per trovare il toret più vicino📍\
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
    bot.send_message(message.chat.id,"Posizione ricevuta")    
    searchnearturet(message.location.latitude, message.location.longitude,message)

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
