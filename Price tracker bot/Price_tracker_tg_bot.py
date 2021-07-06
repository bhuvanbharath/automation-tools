import requests, smtplib, socket, schedule, time
from bs4 import BeautifulSoup
import telebot, validators, re

reqData = []
RunBot = True

API_TOKEN = 'enter bot token here'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global RunBot
    RunBot = True
    if len(reqData)>0:
        reqData.clear()
    msg = bot.send_message(message.chat.id, 'Hi '+message.chat.first_name+', I am Price Alert bot.\n\nPlease enter any product URL from the bigbasket.com website.')
    bot.register_next_step_handler(msg, procees_url_step)

def procees_url_step(message):
    _URL = message.text

    if not validators.url(_URL):
        msg = bot.reply_to(message, "Sorry :(, Invalid URL!\n\nPlease enter the valid URL of the product.")
        bot.register_next_step_handler(msg, procees_url_step)
    else:
        reqData.append(_URL)
        msg = bot.send_message(message.chat.id, 'Enter the ALERT PRICE.\n\nP.S. If the price of the product goes below the Alert price, I will notify you.')
        bot.register_next_step_handler(msg, process_alert_price_step)

def process_alert_price_step(message):
    _alertPrice = message.text

    if _alertPrice.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', _alertPrice):
        reqData.append(_alertPrice)
        msg = bot.send_message(message.chat.id, 'Please enter your mail id. for alerts.')
        bot.register_next_step_handler(msg, procees_mailId_step)
    else:
        msg = bot.reply_to(message, "Sorry :(,\n\nPlease enter the price in number.\n\nEx: 150")
        bot.register_next_step_handler(msg, process_alert_price_step)

def procees_mailId_step(message):
    _mailId = message.text

    if re.match(r"[^@]+@[^@]+\.[^@]+", _mailId):
        reqData.append(_mailId.lower())
        msg = bot.send_message(message.chat.id, "Tracking started...\n\nI will monitor the website twice/day at 09:00 and 21:00 for the price of the product.\n\nI will notify you, if the price drops below the alert price!\n\nPlease check your mail inbox for the ALERTS!\n\n-enter '/stop' to cancel the price monitoring." )
        
        #to monitor the web continuosly
        #schedule.every(30).seconds.do(job, reqData)
        schedule.every().day.at("03:30").do(job, reqData) #UTC time 03:30 == IST time 09:00
        schedule.every().day.at("15:30").do(job, reqData) #UTC time 15:30 == IST time 21:00

        while True:
            #print(RunBot)

            if not RunBot:
                print('Job stopped!')
                schedule.clear()
                #schedule.CancelJob(job)
                break

            time.sleep(1)
            schedule.run_pending()
            
    else:
        msg = bot.reply_to(message, 'Invalid!\nPlease enter the valid mail id.')
        bot.register_next_step_handler(msg, procees_mailId_step)

@bot.message_handler(commands=['stop', 'cancel'])
def Exit_bot(message):
    print ('stop entered')
    global RunBot
    RunBot = False
    bot.send_message(message.chat.id, "The price monitoring has stopped.\n\n-enter '/start' for creating a new alert.")

def job(arr = []):

    print ('Job started')

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
    #print (ConvPrice)
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
    

