from bs4 import BeautifulSoup
from random import randint
import requests
import pandas as pd
import time
from time import sleep
from urllib.parse import urlparse, parse_qs


def sleepms(milliseconds: int):
    seconds = 0.001 * milliseconds
    sleep(seconds)
    
def random_wait():
    start = time.time()
    sleepms(randint(1, 250))

def get_fake_user_agent():
    
    return {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}

def crawl_data(BASE_URL,phone_id):
    price_detail = requests.get(f'{BASE_URL}//model.aspx?modelid={phone_id}',headers = get_fake_user_agent())
    price_soup = BeautifulSoup(price_detail.text, 'html.parser')
    spans = price_soup.find('div',attrs={'class':'prices-txt'}).find_all('span')
    titles = ['מחיר מינימלי','מחיר מקסימלי']
    if len(spans) == 3:
        values = [ spans[1].text, spans[0].text ]
    elif len(spans) == 2: 
        values = [ spans[0].text, spans[0].text ]
    else:
        values = [ None,None ]


    phone_detail = requests.get(f'{BASE_URL}//compmodels.aspx?modelid={phone_id}',headers = get_fake_user_agent())
    phone_soup = BeautifulSoup(phone_detail.text, 'html.parser').find('div',attrs={'class':'compareBox'})
    links = phone_soup.find_all('div', attrs={'class' : 'paramRow'},limit=None)
    
    for i in range(0, len(links)):
        titles.append(links[i].find('div',attrs={'class' : 'ParamCol'}).text.replace('?','').strip())
        values.append(links[i].find('div',attrs={'class' : 'ParamColValue'}).text.strip())
    return dict(zip(titles,values))


def translate_names(df):
    translated_df = pd.DataFrame()
    translation = {
        "יצרן": "Brand",
        "שנת הכרזה": "Out Date",
        "מערכת הפעלה": "Operating System",
        "משקל": "Weight",
        "סדרה": "Series",
        "Smartphone": "Smartphone",
        "ממשק הפעלה": "Operating interface",
        "זיכרון RAM": "RAM Capacity",
        "מהירות מעבד": "CPU speed",
        "דור": "CPU generation",
        "גודל מסך": "Screen Size",
        "מספר ליבות": "Number of cores",
        "רזולוציה": "Screen Resolution",
        "צפיפות פיקסלים": "pixels",
        "קצב רענון": "FPS",
        "סוג מסך": "Screen Type",
        "עמידות במים": "Water resistance",
        "צבעים": "Colors",
        "כרטיס זיכרון": "GPU",
        "מצלמה קדמית": "Front camera",
        "מצלמה": "Camera",
        "קורא טביעת אצבע": "Fingerprint reader",
        "WiFi": "WiFi",
        "מחיר מינימלי": "Min price",
        "מחיר מקסימלי": "Max price",
        "NFC": "NFC",
        "Bluetooth": "Bluetooth",
        "קיבולת הסוללה": "Battery capacity",
        "מספר עמוד": "Page number"}
    df.rename(columns=translation,inplace=True)
    for col in translation.values():
        translated_df[col] = df[col]
    # new_column_names = [translation[col] for col in translation.keys()]
    return translated_df


def zap_data_crawl_all(BASE_URL,filename,page):
    index = page
    df = pd.DataFrame()
    url = f'{BASE_URL}models.aspx?sog=e-cellphone&pageinfo={index}'
    page = requests.get(url,headers = get_fake_user_agent())
    soup = BeautifulSoup(page.text, 'html.parser')
    last_page = int(soup.find('div',attrs={'class':'paging'}).find('select').find_all('option')[-1].text)
    # last_page = 2
    for i in range(index,last_page):
        link_tags = soup.find('div',attrs={'id':'divSearchResults'}).find_all('a')
        phone_id = [link.get('href').split('=')[1].split('&')[0] for link in link_tags]
        for i in range(0, len(phone_id)):
            # print(phone_id[i],flush=True)
            cd = crawl_data(BASE_URL,phone_id[i])
            cd['מספר עמוד'] = index
            df = pd.concat([df,pd.DataFrame([cd])])
        index += 1
        random_wait()
        url = f'{BASE_URL}models.aspx?sog=e-cellphone&pageinfo={index}'
        page = requests.get(url,headers = get_fake_user_agent())
        soup = BeautifulSoup(page.text, 'html.parser')

    translated_df = translate_names(df)
    translated_df.to_csv(filename, index=False ,encoding = 'utf:"8:"sig')

BASE_URL ="https://www.zap.co.il/"
filename = 'phones_data.csv'
page = 1

zap_data_crawl_all(BASE_URL, filename, page)