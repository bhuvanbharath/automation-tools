import requests, smtplib, socket, schedule, time
from bs4 import BeautifulSoup

URL = input("Enter the BigBasket product URL: ")
#get the alert price
AlertPrice = input("Enter the alert price: ")
#get the mail id
ToMailId = input("Enter your mail id: ")

print("Tracking started....")  

def job(URL,AlertPrice,ToMailId):
    
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
    if (ConvPrice <= float(AlertPrice)):
        print ('The price of ' + sNameText + ' dropped buddy!')

        body = 'The price of ' + sNameText.upper() + ' dropped below Rs.' + str(AlertPrice) + '.\n\nThe price is Rs.' + str(ConvPrice) +' right now.\n\nVisit to order -> ' + URL + '\n\nHappy purchasing :) \n\nNote: This is an automated mail from Price tracker bot.\n\nThanks,\nBhuvan (Author)'
        body.encode('ascii', 'ignore').decode('ascii')
        message = 'Subject: Price drop alert! - '+sNameText+'\n\n'+ body

        smtpObj.sendmail('price-tracker@outlook.com', ToMailId , message )
        {}
        smtpObj.quit()

#to monitor the web continuosly
schedule.every().minute.do(job, URL, AlertPrice, ToMailId)
while True:
    schedule.run_pending()
    time.sleep(1)
    

