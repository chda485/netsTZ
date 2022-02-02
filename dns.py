import string, socket, threading
import homoglyphs as hg

from multiprocessing import Process

LOWER_CASE = string.ascii_lowercase
DIGITS = string.digits

DOMENS = ['com', 'ru', 'net', 'org', 'info', 'cn', 'es', 'top', 'au', 'pl', 'it', 'uk',
          'tk', 'ml', 'ga', 'cf', 'us', 'xyz', 'top', 'site', 'win', 'bid' ]

#KEY_WORD = 'group-ib'

#group-ib.ru

def get_id(d):
    try:
        ip = socket.gethostbyname(d)
        print("Domen - {}, ip - {}".format(d, ip))
    except:
        pass
    
def add_domen(word):
    for domen in DOMENS:
        D = str('{}.{}'.format(word, domen))
        potoc = Process(target=get_id, kwargs={'d': D})
        potoc.start()
        potoc.join()

def add_strategy(KEY_WORD):
    for symbol in LOWER_CASE+DIGITS:
        word = KEY_WORD+symbol
        add_domen(word)
            
def homoglyph_strategy(KEY_WORD):
    H = hg.Homoglyphs()
    for letter in KEY_WORD:
        if letter.isdigit() or letter.isalpha():
            comb = H.get_combinations(letter)
            for c in comb:
                word = KEY_WORD.replace(letter, c)
                add_domen(word)
    

def subdomen_strategy(KEY_WORD):
    for i in range(1, len(KEY_WORD)):
        word = KEY_WORD[:i] + "." + KEY_WORD[i:]
        if (".-" in word) or ("-." in word):
            continue
        add_domen(word)
        
        
def delete_strategy(KEY_WORD):
    for i in range(0, len(KEY_WORD)):
        word = KEY_WORD.replace(KEY_WORD[i], '')
        add_domen(word)

def main(word):
    print("Process word - {}".format(word))
    print("Add strategy")
    add_strategy(word.replace(' ', ''))
    print("Homolyph strategy")
    homoglyph_strategy(word.replace(' ', ''))
    print("Subdomen strategy")
    subdomen_strategy(word.replace(' ', ''))
    print("Delete strategy")
    delete_strategy(word.replace(' ', ''))

if __name__ == '__main__':  
    while True:
        KEY_WORD = input("Введите ключевые слова через запятую или q для выхода: ")
        if KEY_WORD == 'q':
            break
        for word in KEY_WORD.split(','):
            word_potoc = Process(target=main, kwargs={'word': word})
            word_potoc.start()
            word_potoc.join()