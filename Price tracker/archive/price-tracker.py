import requests, csv, smtplib, socket, schedule, time, codecs
from bs4 import BeautifulSoup

#get the mail id
ToMailId = input("Enter your mail id: ")
AlertPrice = input("Enter the alert price: ")
print("Tracking started....")  

def main(ToMailId, AlertPrice):

    URL = "https://www.bigbasket.com/pd/10000148/fresho-onion-1-kg/?nc=Best%20Sellers&t_pg=june-t1-home-page&t_p=june-t1-2021&t_s=Best%20Sellers&t_pos_sec=5&t_pos_item=1&t_ch=desktop"
    page = requests.get(URL)
    #print(page.status_code)

    soup = BeautifulSoup(page.content,'html.parser')
    elem = soup.select('._157dw > td:nth-child(2)')
    CurrentPrice = elem[0].getText()
    socket.getaddrinfo('127.0.0.0', 8080)
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtpObj.ehlo()  #to say hello to the connected server
    smtpObj.starttls()  #used for 587 server to ensure encryption
    smtpObj.login('price-tracker@outlook.com', 'Pr!c3tr@cker')

    ConvPrice = float(CurrentPrice.strip('Rs ')) 
    if (ConvPrice <= float(AlertPrice)):
        print ("Price dropped buddy!")

        body = 'The price of onion dropped to ' + str(CurrentPrice) + '.\n\nVisit -> ' + URL + '\nto place an order.\n\nHappy purchasing :)'
        yourstring = body.encode('ascii', 'ignore').decode('ascii')
        message = 'Subject: Price drop alert!\n\n'+ body

        smtpObj.sendmail('price-tracker@outlook.com', ToMailId , message )
        {}
        smtpObj.quit()

def job():
    main(ToMailId, AlertPrice )

schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
#print(soup.prettify())