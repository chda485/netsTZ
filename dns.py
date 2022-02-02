import string, socket, threading
import homoglyphs as hg

from multiprocessing import Process

LOWER_CASE = string.ascii_lowercase
DIGITS = string.digits

DOMENS = ['com', 'ru', 'net', 'org', 'info', 'cn', 'es', 'top', 'au', 'pl', 'it', 'uk',
          'tk', 'ml', 'ga', 'cf', 'us', 'xyz', 'top', 'site', 'win', 'bid' ]

#KEY_WORD = 'group-ib'

#group-ib.ru

"""
function for getting ip address by dn
inputs:
    d: str, dns address
return: 
    void, print result in console
"""
def get_id(d):
    try:
        ip = socket.gethostbyname(d)
        print("Domen - {}, ip - {}".format(d, ip))
    except:
        pass

"""
function search ip through add_strategy
inputs:
    word: str, key_word for dns search
return: 
    void, start processing in separate process
"""
def add_domen(word):
    for domen in DOMENS:
        D = str('{}.{}'.format(word, domen))
        potoc = Process(target=get_id, kwargs={'d': D})
        potoc.start()
        potoc.join()

"""
function search ip through add_strategy
inputs:
    word: str, key_word for dns search
return: 
    void, start processing in separate process
"""
def add_strategy(KEY_WORD):
    for symbol in LOWER_CASE+DIGITS:
        word = KEY_WORD+symbol
        add_domen(word)

"""
function search ip through homogliph_strategy
inputs:
    word: str, key_word for dns search
return: 
    void, start processing in separate process
"""         
def homoglyph_strategy(KEY_WORD):
    #create homogligh object
    H = hg.Homoglyphs()
    for letter in KEY_WORD:
        #if it is digit or letter< not -,_
        if letter.isdigit() or letter.isalpha():
            #get all homoglyph for the letter
            comb = H.get_combinations(letter)
            for c in comb:
                word = KEY_WORD.replace(letter, c)
                add_domen(word)

"""
function search ip through subdomen_strategy
inputs:
    word: str, key_word for dns search
return: 
    void, start processing in separate process
"""
def subdomen_strategy(KEY_WORD):
    for i in range(1, len(KEY_WORD)):
        word = KEY_WORD[:i] + "." + KEY_WORD[i:]
        if (".-" in word) or ("-." in word):
            continue
        add_domen(word)

"""
function search ip through delete_strategy
inputs:
    word: str, key_word for dns search
return: 
    void, start processing in separate process
"""      
def delete_strategy(KEY_WORD):
    for i in range(0, len(KEY_WORD)):
        word = KEY_WORD.replace(KEY_WORD[i], '')
        add_domen(word)


"""
function for starting processing the word through startegies
inputs:
    word: str, key_word for dns search
return: 
    void, start diffirent strategies
"""
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
        #start process each word in separate process
        for word in KEY_WORD.split(','):
            word_potoc = Process(target=main, kwargs={'word': word})
            word_potoc.start()
            word_potoc.join()