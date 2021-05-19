import requests
from bs4 import BeautifulSoup
import smtplib
import time as t
from datetime import datetime, time
import sender

carriers = {
	'att':    '@txt.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def send(message):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
	to_number = '1234567890{}'.format(carriers['att'])
	auth = ('gmail account', 'Password')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number, message)

sent = False
reqCount = 3
sender.post_url("https://www.newegg.com/")
while (True):
    try:
        inRange = is_time_between(time(9,0),time(9,10))
        if(inRange and not sent):
            send(str(reqCount) + ' Pages scraped yesterday')
            reqCount = 0
            sent = True
        if(not inRange and sent):
            sent = False

    ######################################### EVGA ############################################
        print('\033[0m')
        page = requests.get('https://www.evga.com/products/productlist.aspx?type=0&family=GeForce+30+Series+Family', headers={'User-Agent': 'Mozilla/5.0'})
        print('Evga ' + str(page) + ' : ' + str(datetime.now()))
        reqCount += 1
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='list-item')
        for p in results:
            name = p.find(class_='pl-list-pn').text
            status = 'Out of Stock' in p.find(class_='message').text.strip()
            printStatus = ('In Stock', 'Out of Stock')[status]
            print(('\033[92m','\033[91m')[status] + ' ' + name + ' ' + printStatus)
            if(not status):
                send('Found in stock on evga ' + name.split(':')[1])
                t.sleep(2)

    ######################################## Newegg ##########################################
        print('\033[0m')
        page = requests.get('https://www.newegg.com/p/pl?d=gigabyte+2070+super', headers={'User-Agent': 'Mozilla/5.0'})
        print('Newegg ' + str(page) + ' : ' + str(datetime.now()))
        reqCount += 1
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='item-cell')
        for p in results:
            name = p.find(class_='item-title', href=True)
            status = False
            for ip in p.find_all(class_='item-promo', href=True):
                if 'OUT OF STOCK' in ip.text:
                    status = True
                    break 
            printStatus = ('In Stock', 'Out of Stock')[status]
            print(('\033[92m','\033[91m')[status] + ' ' + name.text[:25] + ' ' + printStatus)
            if(not status):
                print(name['href'])
                send('Found in stock on newegg ' + name.text[:25])
                sender.post_url(name['href'])
                t.sleep(2)

    ######################################## BestBuy ##########################################
        print('\033[0m')
        page = requests.get('https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080', headers={'User-Agent': 'Mozilla/5.0'})
        print('BestBuy ' + str(page) + ' : ' + str(datetime.now()))
        reqCount += 1
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='sku-item')
        for p in results:
            name = p.find(class_='sku-title').find('a').text
            txt = p.find(class_='fulfillment-add-to-cart-button').find('button').text.strip()
            status = 'Sold Out' in txt or 'Coming Soon' in txt
            printStatus = ('In Stock', 'Out of Stock')[status]
            print(('\033[92m','\033[91m')[status] + ' ' + name[:25] + ' ' + printStatus)
            if(not status):
                send('Found in stock on bestbuy ' + name[:20])
                t.sleep(2)
    except:
        pass
    t.sleep(30)