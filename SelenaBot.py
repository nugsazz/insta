#! python3

'''
BeautifulSoup Instagram Scraper that gets all pictures posted by celebrities yeterday (max 12 pictures per celeb)
'''

import requests, json, webbrowser, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from top100gram import top100

instagram = 'http://www.instagram.com/' 
yesterday = (datetime.today()- timedelta(days=1)).strftime('%Y-%m-%d') 
filepath = os.path.join('.','SelenaBot_Pictures',yesterday)

if os.path.exists(filepath) == False:
    os.makedirs(filepath) 

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def SelenaBot(account):
    try:
        rgram = requests.get(instagram + account)
        rgram.raise_for_status()
    except requests.exceptions.HTTPError:	#this handles exceptions if accounts get deleted or suspended. Does not handle exceptions for accounts made private
        print('\t \t ### ACCOUNT MISSING ###')
    else:
        rgram = requests.get(instagram + account) #opens specific instagram account
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        allPics= json.loads(str(pageJS[6])[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes'] # pulls out information on most recent 12 pictures into a list called "All Pics"
        for picture in allPics:            
            if datetime.fromtimestamp(picture['date']).strftime('%Y-%m-%d') == yesterday: #finds pictures from yesterday
                print('\tDownloading picture '+DateStamp(picture['date']))
                #webbrowser.open(picture['display_src']) #kept here for debugging
                picRes = requests.get(picture['display_src'])
                picFileName = os.path.join(filepath, account+'_'+DateStamp(picture['date'])+'.jpg')
                picFile = open(picFileName,'wb')

                for chunk in picRes.iter_content(100000):
                    picFile.write(chunk)

                picFile.close()

print(os.getcwd())
                                    
for account in top100:
    print('Pictures from today on '+account+'\'s Instagram')
    SelenaBot(account)

print('Files saved in: ' +os.path.abspath(filepath))  #clungy debug so I can check where it's saving things whilst I'm not looking
c = True
if c == True:
    print('press any key to close')
    c = input()
