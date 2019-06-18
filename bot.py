
import telebot
import os
import time
import random
import sqlite3

from bs4 import BeautifulSoup
from urllib.request import *
import urllib.request
import re

import config
from SQLighter import SQLighter

bot = telebot.TeleBot(config.token)




# получение кода html
def get_html(url):
    # типо как обход какой-то защиты чтобы наебать сайт
    opener = build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0')]
    install_opener(opener)
    # загрузка страницы
    req = Request(url)
    # считывание html
    html = urlopen(req).read()
    # перевод из bytes в str
    text_parser = html.decode()
    return text_parser

# проверка на существование аккаунта
def check_account(url_account):
    try:
        html = get_html('https://www.instagram.com/'+url_account)
    except:
        # если страницы не существует
        return False
    result = re.search('К сожалению, эта страница недоступна.',html)
    # false - нету аккаунта или недоступен, true существует 
    if result == '':
        return False
    else:
        return True





    


    # # Получаем случайную строку из БД
    # row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # # Формируем разметку
    # markup = utils.generate_markup(row[2], row[3])
    # # Отправляем аудиофайл с вариантами ответа
    # bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # # Включаем "игровой режим"
    # utils.set_user_game(message.chat.id, row[2])
    
# команда начала
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
    ''' Бот rdy\n/track - отслеживание аккаунта
        
        ''')


    
#чистит стоку от пробелов и прочего шлака. В text записыпается только краткую ссылку
def str_clear(text): 
    text = re.sub(r'\s+', ' ', text) #удаление лишних пробелов 
    text = text.replace('https://www.instagram.com/','')
    text = text.replace('/','')
    text = text.strip(' ')#удаление пробелов в начале и конце строки
    return text

# поиск ссылки последнего поста в html коде
def find_link_last_post(short_url_account):
    text = get_html('https://www.instagram.com/'+short_url_account)
    text = re.sub(r'"',' ',text)
    text = re.split(r' ',text)
    # Не спрашивай как это работает
    x = 0
    for j in text:
        result = re.findall(r'https:.*1080x1080.*com', j)
        for i in result:
            x = x+1
            if x==3:
                return i

# поиск ссылки последней истории в html коде 
def find_link_last_story(short_url_account):
    # перекодируется из строки в байты 
    html = get_html('https://www.instagram.com/'+short_url_account).encode('utf-8')
    soup = BeautifulSoup(html)
    video = soup.find('video', class_='y-yJ5 OFkrO')
    print(video)



    result = re.findall(r'http.*\.mp4.*"', html)
    print(result)
    return result



#команда для отслеживания аккаунтов
@bot.message_handler(commands=['track'])
def start_message(message):
    # обрезка команды в тексте пользователя
    short_url_account = message.text[7:]
    # проверка на правильность ввода команды
    if  len(short_url_account) == 0:
        bot.send_message(message.chat.id,'Введите адрес аккаунта')
        return
    # проверка на ввод полной ссылки или краткой 
    if '/' or ' 'in short_url_account :
        short_url_account = str_clear(short_url_account)
    # проверка на существование аккаунта
    if check_account(short_url_account) == False:
        bot.send_message(message.chat.id,'Неккоректный адрес аккаунта')
        return  
    # запись имени пользователя
    username = message.from_user.username
    # запись имени отслежимаемого аккаунта
    track_accouunt = message.text[6:]
    # поиск ссылки последнего поста в html коде
    link_last_post = find_link_last_post(short_url_account)
    # поиск ссылки последней истории в html коде
    link_last_story = find_link_last_story(short_url_account)
    print('1-'+username+'\n')
    print('1-'+track_accouunt+'\n')
    print('1-'+link_last_post+'\n')
    print('1-'+link_last_story+'\n')





    bot.send_message(message.chat.id, '1-'+username+'\n2-'+track_accouunt)
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Отсоединяемся от БД
    db_worker.close()


if __name__ == '__main__':
     bot.polling(none_stop=True)