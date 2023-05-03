from bs4 import BeautifulSoup
from random import randint
import requests
import pandas as pd
import time
from time import sleep
from urllib.parse import urlparse, parse_qs


# def sleepms(milliseconds: int):
#     seconds = 0.001 * milliseconds
#     sleep(seconds)
    
# def random_wait():
#     # start = time.time()
#     sleepms(5000+randint(1, 250))

# def get_fake_user_agent():
    
#     return {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}

# def zap_crawl_data(BASE_URL,phone_id):
#     price_detail = requests.get(f'{BASE_URL}//model.aspx?modelid={phone_id}',headers = get_fake_user_agent())
#     price_soup = BeautifulSoup(price_detail.text, 'html.parser')
#     spans = price_soup.find('div',attrs={'class':'prices-txt'}).find_all('span',limit=None)
#     titles = ['מחיר מינימלי','מחיר מקסימלי']
#     if len(spans) == 3:
#         values = [ spans[1].text, spans[0].text ]
#     elif len(spans) == 2: 
#         values = [ spans[0].text, spans[0].text ]
#     else:
#         values = [ None,None ]


#     phone_detail = requests.get(f'{BASE_URL}//compmodels.aspx?modelid={phone_id}',headers = get_fake_user_agent())
#     phone_soup = BeautifulSoup(phone_detail.text, 'html.parser').find('div',attrs={'class':'compareBox'})
#     links = phone_soup.find_all('div', attrs={'class' : 'paramRow'},limit=None)
    
#     for i in range(0, len(links)):
#         titles.append(links[i].find('div',attrs={'class' : 'ParamCol'}).text.replace('?','').strip())
#         values.append(links[i].find('div',attrs={'class' : 'ParamColValue'}).text.strip())

#     return dict(zip(titles,values))

# def translate_names(df):
#     translated_df = pd.DataFrame()
#     translation = {
#         "יצרן": "Brand",
#         "שנת הכרזה": "Out Date",
#         "מערכת הפעלה": "Operating System",
#         "משקל": "Weight",
#         "סדרה": "Series",
#         "Smartphone": "Smartphone",
#         "ממשק הפעלה": "Operating interface",
#         "זיכרון RAM": "RAM Capacity",
#         "מהירות מעבד": "CPU speed",
#         "דור": "CPU generation",
#         "גודל מסך": "Screen Size",
#         "מספר ליבות": "Number of cores",
#         "רזולוציה": "Screen Resolution",
#         "צפיפות פיקסלים": "pixels",
#         "קצב רענון": "FPS",
#         "סוג מסך": "Screen Type",
#         "עמידות במים": "Water resistance",
#         "צבעים": "Colors",
#         "כרטיס זיכרון": "GPU",
#         "מצלמה קדמית": "Front camera",
#         "מצלמה": "Camera",
#         "קורא טביעת אצבע": "Fingerprint reader",
#         "WiFi": "WiFi",
#         "מחיר מינימלי": "Min price",
#         "מחיר מקסימלי": "Max price",
#         "NFC": "NFC",
#         "Bluetooth": "Bluetooth",
#         "קיבולת הסוללה": "Battery capacity",
#         "מספר עמוד": "Page number"}
#     df.rename(columns=translation,inplace=True)
#     for col in translation.values():
#         translated_df[col] = df[col]
#     # new_column_names = [translation[col] for col in translation.keys()]
#     return translated_df


# def zap_data_crawl_all(BASE_URL,filename,page):
#     index = page
#     df = pd.DataFrame()
#     url = f'{BASE_URL}models.aspx?sog=e-cellphone&pageinfo={index}'
#     page = requests.get(url,headers = get_fake_user_agent())
#     soup = BeautifulSoup(page.text, 'html.parser')
#     last_page = int(soup.find('div',attrs={'class':'paging'}).find('select').find_all('option',limit=None)[-1].text)
#     for i in range(index,last_page):
#         a_tags = soup.find('div',attrs={'id':'divSearchResults'}).find_all('a',limit=None)
#         phone_id = [tag.get('data-model-id') for tag in a_tags] 
#         for i in range(0, len(phone_id)):
#             cd = zap_crawl_data(BASE_URL,phone_id[i])
#             if(cd is not None):
#                 cd['מספר עמוד'] = index
#                 df = pd.concat([df,pd.DataFrame([cd])])
#         index += 1
#         random_wait()
#         url = f'{BASE_URL}models.aspx?sog=e-cellphone&pageinfo={index}'
#         page = requests.get(url,headers = get_fake_user_agent())
#         soup = BeautifulSoup(page.text, 'html.parser')
#     translated_df = translate_names(df)
#     translated_df.to_csv(filename, index=False, mode='a', header=False ,encoding = 'utf:"8:"sig')

# ZAP_BASE_URL ="https://www.zap.co.il/"
# zap_filename = 'zap_data.csv'
# zap_page = 22

# # zap_data_crawl_all(BASE_URL=ZAP_BASE_URL, filename=zap_filename, page=zap_page)

# # ------------------Ret--------------------
# def ret_crawl_data(BASE_URL,phone_id):
#     url = f'{BASE_URL}m/{phone_id}/specs'
#     page = requests.get(url,headers = get_fake_user_agent())
#     soup = BeautifulSoup(page.text, 'html.parser')
#     meta = soup.find('div',attrs={'class','price'})
#     lowPrice = meta.find('meta',attrs={'itemprop':'lowPrice'})
#     highPrice = meta.find('meta',attrs={'itemprop':'highPrice'})
#     if(lowPrice == None or highPrice == None):
#         return None
#     titles = ['מחיר מינימלי','מחיר מקסימלי']
#     values = [lowPrice.get('content'),highPrice.get('content')]
#     properties = soup.find('div',attrs={'class','single-product-tab'}).find_all('ul',attrs={'class':'list-group list-group-horizontal'},limit=None)
#     for i in range(0,len(properties)):
#         [title,value] = properties[i].find_all('li',limit=None)
#         titles.append(title.text.strip())
#         values.append(value.text.strip()) 
    
#     return dict(zip(titles,values))

# def ret_data_crawl_all(BASE_URL,filename,page):
#     index = page
#     df = pd.DataFrame()
#     url = f'{BASE_URL}shop/cellphone?pageindex={index}'
#     page = requests.get(url,headers = get_fake_user_agent())
#     soup = BeautifulSoup(page.text, 'html.parser')
#     last_page =  int(soup.find('nav',attrs={'class':'card-pagination'}).find('div').text.split(' ')[-1])
#     for i in range(index,last_page+1):
#         phone_divs = soup.find('div',attrs={'class':'product-list'}).find_all('div',attrs={'class':'shop-block'},limit=None)
#         phone_id = [div.get('data-id') for div in phone_divs]
#         for i in range(0, len(phone_id)):
#             cd = ret_crawl_data(BASE_URL,phone_id[i])
#             if(cd is not None):
#                 cd['מספר עמוד'] = index
#                 df = pd.concat([df,pd.DataFrame([cd])])
#         index += 1
#         random_wait()
#         url = f'{BASE_URL}shop/cellphone?pageindex={index}'
#         page = requests.get(url,headers = get_fake_user_agent())
#         soup = BeautifulSoup(page.text, 'html.parser')
#     translated_df = translate_names(df)
#     translated_df.to_csv(filename, index=False,mode='a', header=False,encoding = 'utf:"8:"sig')    


# RET_BASE_URL = "https://www.ret.co.il/"
# ret_filename = 'ret_data.csv'
# ret_page = 11
# ret_data_crawl_all(BASE_URL=RET_BASE_URL, filename=ret_filename, page=ret_page)

df = pd.read_csv('./data/zap_data.csv')
df['Page number'] = pd.to_numeric(df['Page number'])
df.sort_values(['Page number'],inplace=True)

df.to_csv('./data/zap_data1.csv',index=False)