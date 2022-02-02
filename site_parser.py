import requests, re, json, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time, datetime, threading
from google_play_scraper import app
from multiprocessing import Process

BASE_URL = r'https://play.google.com'
SEARCH_TEMPLATE = r'/store/search?q={}&c=apps'
URL_SEARCH_TEMPLATE = '/store/apps/.*></a>'
GLOBAL_JSON = []

"""
function compile reqex object
inputs:
    word: str, key_word for search
return: 
    reqex: Regex-object, object to search word in string
"""
def make_search_regex(word):
    regex = re.compile(word + '.{0,2}')
    return regex

"""
function make url
inputs:
    word: str, key_word for search
return: 
    url: str, url-string of search page
"""
def get_page_with_list(word):
    url = BASE_URL + SEARCH_TEMPLATE.format(word.lower())
    return url

"""
function check if word in title and description
inputs:
    word: str, key_word for search
    info: object, parsed info about app
return: 
    bool, status if word is in
"""    
def check_keyword_isin(info, word):
    regex = make_search_regex(word)
    if len(regex.findall(info['title'].lower() + info[
            'description'].lower())) !=0:
        return True
    else:
        return False

"""
function scrap info about app
inputs:
    word: str, key_word for search
    url: str, url-address app in google play directories
return: 
    void: add info in global list
"""
def scrap_page(url, word):
    global GLOBAL_JSON
    info = {}
    #get name for api parser
    name=url.split('=')[1]
    #print(name)
    try:
        result = app(str(name))
        #if key word is in title and description
        if check_keyword_isin(result, word):
            info['Название'] = result['title']
            info['Ссылка']  = result['url']
            info['Автор']  = result['developer']
            info['Категория']  = result['genre']
            info['Описание']  = result['description']
            info['Средняя оценка']  = result['score']
            info['Количество оценок']  = result['ratings']
            info['Число обзоров']  = result['reviews']
            info['Последнее обновление']  = datetime.datetime.fromtimestamp(result['updated']).strftime(
                "%A, %B %d, %Y %I:%M:%S")
            #add info in global JSON -object
            json_info = json.dumps(info)
            json_info = json.loads(json_info)
            GLOBAL_JSON.append(json_info)
    except:
        pass
 
"""
function parse search page
inputs:
    word: str, key_word for search
return: 
    void: start processing pages in separate processes
"""       
def parse_search(word):
    #make the options for start browser in background
    opts = Options()
    opts.add_argument("--headless")
    url = get_page_with_list(word)
    #service for the browser to start
    service = Service(r'nets/geckodriver')
    #start the browser
    driv = webdriver.Firefox(service=service, options=opts)
    driv.get(url)
    last_height = driv.execute_script("return document.body.scrollHeight")

    #list the page to the bottom and grap all search pages
    while True:
        driv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driv.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    #get html
    soup = BeautifulSoup(driv.page_source, 'html.parser')
    s = []
    driv.close()

    #get all links to apps
    for link in soup.findAll('a'):
        l = link.get('href')
        if l.startswith('/store/apps/details'):
            s.append(l)
    s = list(set(s))
    for link in s:
        potoc = Process(target=scrap_page, kwargs={'url': link, 'word': word})
        potoc.start()
        potoc.join()

if __name__ == '__main__': 
    while True:
        word = input("Введите ключевое слово поиска или q для выхода: ")
        if word == 'q':
            break
        #parse search page
        parse_search(word)
        #if file exist from last works, delete it
        if os.path.exists('itcome.json'):
            os.remove('itcome.json')
        f = open('itcome.json', 'a')
        #write all json in json file
        for item in GLOBAL_JSON:
            #print(item['Название'])
            item = json.dumps(item, ensure_ascii=False)
            item = json.loads(item)
            json.dump(item, f, ensure_ascii=False)
        f.close()
        print("Файл вывода - {}".format(os.getcwd()+'/itcome.json'))




