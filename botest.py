import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import radians, cos, sin, asin, sqrt
from urllib.request import urlopen
import requests
import json


FILENAME = ""
API_TOKEN = ':'
bot = telebot.TeleBot(API_TOKEN)
totalmap_string="Mappa completa dei toret"
def leggidati(file_name):
    
    dati = []

    try:
        fountains_file = json.loads(requests.get(FILENAME).text)
    except:
        print("errore file json")

    dim=len(fountains_file)
    for i in range(dim):
        value=[]
        lng=float(fountains_file[i]['latlng']['longitude'])
        value.append(lng)
        lat=float(fountains_file[i]['latlng']['latitude'])
        value.append(lat)
        name=str(fountains_file[i]['address'])
        value.append(name)
        dati.append(value)

    return dati

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    itembtn1 = types.KeyboardButton('Manda La tua posizione', request_location=True)
    itembtn2 = types.KeyboardButton(totalmap_string)
    itembtn3 = types.KeyboardButton("Help")
    markup.add(itembtn1,itembtn2,itembtn3)
    #print(message)
    username=str(message.from_user.first_name)
    bot.send_message(message.chat.id,"Ciao "+username+", benvenuto al turin toret bot")
    bot.send_message(message.chat.id, """Se vi dicessimo che il simbolo di Torino non è la Mole Antonelliana, ma i toret? Cosa sono i "toret"? Ve lo sveliamo subito. 
    Si tratta delle tipiche fontanelle color verde bottiglia che come bocchettoni d’acqua hanno una testa di toro. Il torèt compare sempre più spesso nei negozi che promuovo i souvenir di Torino accanto ovviamente a quelli raffiguranti la Mole, il grande classico dei gadget.\
""")
    bot.send_photo(message.chat.id, 'https://i.pinimg.com/750x/f7/26/63/f726638483f45169631dcfa425261969.jpg')
    bot.send_message(message.chat.id,username+" digita /help per ricevere la lista di comandi utili per usare il bot")
    bot.reply_to(message,username+ " per favore mandami la tua posizione per trovare il toret più vicino📍")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,"""Sono disponibili i seguenti comandi:
        /start -> Messaggio di benvenuto 
        /help -> aiuto.
        /associazione -> link per il sito i love toret
        /mappa -> link per la mappa di tutti i toret
        /contact -> Messaggio con tutti i contatti di i love toret
    """)

@bot.message_handler(commands=['associazione'])
def send_associazione(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Sito", url='https://ilovetoret.it'))
    bot.send_message(message.chat.id, "Ecco qua⬇️", reply_markup=markup)

@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message,"""Creatore Bot: Simone Candido
    Mail: candidosimone598@gmail.com
    Telegram: @Simonecandido
    Instagram: @simocandido

Associazione i love toret
    Sede legale: Via Vittorio Andreis 18/16s, Torino, Italia
    Mail: info@ilovetoret.it
    Instagram: @ilovetoret  
    """)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if (message.text)=="Help":
        send_help(message)
    elif (message.text)!=totalmap_string and (message.text)!="/mappa":
        bot.reply_to(message,"""Non riesco a capire, per favore mandami la tua posizione per trovare il toret più vicino📍\
""")
    else:
        sendlinkmap(message)
 
 #in questo modo mando la posizione tramite send_location e per ricavare le latitudini e longitudine utilizzo il campo 'location' e lat o lng ecc...
 #la parte importante è la prima riga in cui devo specificicare il content_types=["location"]
@bot.message_handler(content_types=["location"])
def location_received(message):
    bot.send_message(message.chat.id,"Posizione ricevuta")    
    searchnearfountains(message.location.latitude, message.location.longitude,message)

def searchnearfountains(lat_current,lng_current,message):
    dati=leggidati(FILENAME)
    rmb=mindistancefountains(dati,lat_current,lng_current)
    lng_result=dati[rmb][0]
    lat_result=dati[rmb][1]
    name_result=dati[rmb][2]
    username=str(message.from_user.first_name)
    bot.send_location(message.chat.id,  lat_result , lng_result)
    bot.send_message(message.chat.id,"Ecco il toret più vicino " + username +" :)")
    bot.send_message(message.chat.id,"Distanza: "+str(round(distance(lat_current,lng_current,lat_result,lng_result))) + "m")
    bot.send_message(message.chat.id,name_result)

def mindistancefountains(dati,lat_current,lng_current):
    minima_distance=pow(pow(lat_current - dati[0][1], 2) + pow(lng_current - dati[0][0], 2), .5)
    countrmb=0
    for value in dati:
        distance=pow(pow(lat_current - value[1], 2) + pow(lng_current - value[0], 2), .5)
        if(distance<minima_distance):
            minima_distance=distance
            rmb=countrmb
        countrmb=countrmb+1
    return rmb

def distance(lat1,lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return((c * r)*1000)

def sendlinkmap(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Mappa", url='https://ilovetoret.it/it/mappa/'))
    bot.send_message(message.chat.id, "Ecco qua⬇️", reply_markup=markup)

bot.infinity_polling()
