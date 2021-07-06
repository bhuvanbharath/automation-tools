import requests, smtplib, socket, schedule, time
from bs4 import BeautifulSoup
import telebot, validators, re

reqData = []

API_TOKEN = '1896398292:AAGOEbVFchgBI2si4vFFmmKoCD4FMeX9wSs'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    
    msg = bot.reply_to(message, 'Hi there, I am Price Alert bot.\nPlease enter the BIG BASKET product URL.')
    bot.register_next_step_handler(msg, procees_url_step)

def procees_url_step(message):
    _URL = message.text
    print (_URL)

    if not validators.url(_URL):
        msg = bot.reply_to(message, 'Invalid URL!\nPlease enter the valid URL of the product.')
        bot.register_next_step_handler(msg, procees_url_step)
    else:
        reqData.append(_URL)
        msg = bot.reply_to(message, 'Enter the alert price.')
        bot.register_next_step_handler(msg, process_alert_price_step)

def process_alert_price_step(message):
    _alertPrice = message.text
    print (_alertPrice)

    if _alertPrice.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', _alertPrice):
        reqData.append(_alertPrice)
        msg = bot.reply_to(message, 'Please enter the your mail id.')
        bot.register_next_step_handler(msg, procees_mailId_step)
    else:
        msg = bot.reply_to(message, 'Invalid!\nPlease enter the price in number.')
        bot.register_next_step_handler(msg, process_alert_price_step)

def procees_mailId_step(message):
    
    _mailId = message.text
    print (_mailId)

    if not re.match(r"[^@]+@[^@]+\.[^@]+", _mailId):
        msg = bot.reply_to(message, 'Invalid!\nPlease enter the valid mail id.')
        bot.register_next_step_handler(msg, procees_mailId_step)
    else:
        reqData.append(_mailId.lower())
        msg = bot.reply_to(message, "Tracking started...\n\nI will notify you if the price drops!\n\nPlease check your mail id for ALERTS!\n\n-enter '/start' for creating a new alert." )

        #to monitor the web continuosly
        schedule.every(20).seconds.do(job, reqData)

        while True:
            schedule.run_pending()
            time.sleep(1)   


def job(arr = []):
    
    print ('job func entered.')
    print (arr[0])
    print (arr[1])
    print (arr[2])

    URL = arr[0]
    AlertPrice = arr[1]
    ToMailId = arr[2]

    page = requests.get(URL)    
    soup = BeautifulSoup(page.content,'html.parser')
    
    #get the product name
    NameElem = soup.find('h2' ,attrs={'class':'_25I07'})
    NameText = NameElem.renderContents()
    sNameText = str(NameText).strip("b'")

    #get the product price
    PriceElem = soup.find('td' ,attrs={'class':'IyLvo'})
    PriceText = PriceElem.renderContents()
    sPriceText = str(PriceText).strip("b'Rs <!->")

    #mail connection
    socket.getaddrinfo('127.0.0.0', 8080)
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtpObj.ehlo()  #to say hello to the connected server
    smtpObj.starttls()  #used for 587 server to ensure encryption
    smtpObj.login('price-tracker@outlook.com', 'Pr!c3tr@cker')

    ConvPrice = float(sPriceText)
    print (ConvPrice)
    if (ConvPrice <= float(AlertPrice)):
        print ('The price of ' + sNameText + ' dropped buddy!')

        body = 'The price of ' + sNameText.upper() + ' dropped below Rs.' +str(AlertPrice) + '.\n\nThe price is Rs.' + str(ConvPrice) +' right now.\n\nVisit to order -> ' + URL + '\n\nHappy purchasing :) \n\nNote: This is an automated mail from Price tracker bot.\n\nThanks,\nBhuvan (Author)'
        #body.encode('ascii', 'ignore').decode('ascii')
        MailMessage = 'Subject: Price drop alert! - '+sNameText+'\n\n'+ body

        smtpObj.sendmail('price-tracker@outlook.com', ToMailId , MailMessage )
        {}
        smtpObj.quit()

while True:
    try:
        bot.polling()
    except:
        time.sleep(1)
    

