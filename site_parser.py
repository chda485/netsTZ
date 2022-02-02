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

def make_search_regex(word):
    regex = re.compile(word + '.{0,2}')
    return regex

def get_page_with_list(word):
    url = BASE_URL + SEARCH_TEMPLATE.format(word.lower())
    return url
    
def check_keyword_isin(info, word):
    regex = make_search_regex(word)
    if len(regex.findall(info['title'].lower() + info[
            'description'].lower())) !=0:
        return True
    else:
        return False
       
def scrap_page(url, word):
    global GLOBAL_JSON
    info = {}
    name=url.split('=')[1]
    #print(name)
    try:
        result = app(str(name))
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
            json_info = json.dumps(info)
            json_info = json.loads(json_info)
            GLOBAL_JSON.append(json_info)
    except:
        pass
        
def parse_search(word):
    opts = Options()
    opts.add_argument("--headless")
    url = get_page_with_list(word)
    
    service = Service(r'nets/geckodriver')

    driv = webdriver.Firefox(service=service, options=opts)
    driv.get(url)
    last_height = driv.execute_script("return document.body.scrollHeight")

    while True:
        driv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driv.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driv.page_source, 'html.parser')
    s = []
    driv.close()

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
        parse_search(word)
        if os.path.exists('itcome.json'):
            os.remove('itcome.json')
        f = open('itcome.json', 'a')
        for item in GLOBAL_JSON:
            #print(item['Название'])
            item = json.dumps(item, ensure_ascii=False)
            item = json.loads(item)
            json.dump(item, f, ensure_ascii=False)
        f.close()
        print("Файл вывода - {}".format(os.getcwd()+'/itcome.json'))




