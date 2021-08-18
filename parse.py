import telebot
import sqlite3
from telebot import types
from random import randint
from config import *
from words import allWords

TOKEN = '1916257391:AAElNrLgDs7U11_jYUuvjXas0Dn3-sN3JUs'

bot = telebot.TeleBot(TOKEN)

wordArr = []


global db
global sql

db = sqlite3.connect('botUsers.db', check_same_thread=False)
sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER,
                            name TEXT,
                            word INTEGER,
                            randword INTEGER);'''

sql = db.cursor()
sql.execute(sqlite_create_table_query)
db.commit()

keyboard = types.ReplyKeyboardMarkup(True)
keyboard.add('Слова', 'Рандомные слова')
keyboard.add('Обнулить слова', 'Обнулить рандомные слова')
keyboard.add('Сколько изучил', 'Сколько изучил рандомных')
keyboard.add('Изучить времена')

@bot.message_handler(commands=['start'])
def send_mess(message):
    
    userId = int(message.from_user.id)
    userName = message.from_user.username
    userWord = 0
    userRandWord = 0
    bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}', reply_markup=keyboard)
    
    
    sql.execute(f"SELECT id FROM users WHERE id = {userId}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (userId, userName, userWord, userRandWord))
        db.commit()
        print("Зареган")
    else:
        for value in sql.execute("SELECT * FROM users"):
            print(value)


@bot.message_handler(content_types=['text'])
def send_word(message):
    userId = message.from_user.id

    parseMinWord = sql.execute(f"SELECT word FROM users WHERE id = {userId}")
    parseMinWord = sql.fetchone()
    pMinW = parseMinWord[0]
    pMaxW = pMinW + 10

    parseRandWord = sql.execute(f"SELECT randword FROM users WHERE id = {userId}")
    parseRandWord = sql.fetchone()
    pRandW = parseRandWord[0]


    if message.text == 'Рандомные слова':
        for i in range(1, 11):
            num = randint(1, 4999)
            wordArr.append(allWords[num])
        for i in wordArr:
            for item in i.items():
                engWord = item[0]
                rusWord = item[1]
                bot.send_message(message.chat.id, f'{engWord} : {rusWord}')

        mainRandWord = sql.execute(f"SELECT randword FROM users WHERE id = {userId}")
        mainRandWord = sql.fetchone()
        wordArr.clear()
        mRW = mainRandWord[0]

        if mRW == 5000:
            mRW = 0
        else:
            mRW += 10

        sql.execute(f"SELECT id FROM users WHERE id = {userId}")
        if sql.fetchone() is None:
            print("Такого нет!")
        else:
            sql.execute(f"UPDATE users SET randword = {mRW} WHERE id = {userId}")
            db.commit()


    elif message.text == 'Слова':
        for i in range(pMinW, pMaxW):
            wordArr.append(allWords[i])

        for i in wordArr:
            for item in i.items():
                engWord = item[0]
                rusWord = item[1]
                bot.send_message(message.chat.id, f'{engWord} : {rusWord}')

        mainWord = sql.execute(f"SELECT word FROM users WHERE id = {userId}")
        mainWord = sql.fetchone()
        wordArr.clear()
        mW = mainWord[0]

        if mW == 5000:
            mW = 0
        else:
            mW += 10

        sql.execute(f"SELECT id FROM users WHERE id = {userId}")

        if sql.fetchone() is None:
            print("Такого нет!")
        else:
            sql.execute(f"UPDATE users SET word = {mW} WHERE id = {userId}")
            db.commit()


    elif message.text == 'Сколько изучил':
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы изучили уже {pMinW} слов')


    elif message.text == 'Сколько изучил рандомных':
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы изучили уже {pRandW} слов')


    elif message.text == 'Обнулить слова':
        keyboardSure = types.ReplyKeyboardMarkup(True)
        keyboardSure.add('Да, я уверен!')
        keyboardSure.add('Нет, я не хочу!')
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы уверены что хотите обнулить слова?', reply_markup=keyboardSure)


    elif message.text == 'Да, я уверен!':
        sql.execute(f"UPDATE users SET word = {0} WHERE id = {userId}")
        db.commit()
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы успешно обнулили слова {pMinW}', reply_markup=keyboard)
    
    
    elif message.text == 'Нет, я не хочу!':
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы отменили обнуление слов {pMinW}', reply_markup=keyboard)
    
    
    elif message.text == 'Обнулить рандомные слова':
        keyboardRandSure = types.ReplyKeyboardMarkup(True)
        keyboardRandSure.add('Да, я хочу обнулить рандомные слова!')
        keyboardRandSure.add('Нет, я не хочу обнулять рандомные слова!')
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы уверены что хотите обнулить рандомные слова?', reply_markup=keyboardRandSure)
    
    
    elif message.text == 'Да, я хочу обнулить рандомные слова!':
        sql.execute(f"UPDATE users SET randword = {0} WHERE id = {userId}")
        db.commit()
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы успешно обнулили рандомные слова {pRandW}', reply_markup=keyboard)
    
    
    elif message.text == 'Нет, я не хочу обнулять рандомные слова!':
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}, вы отменили обнуление рандомных слов {pRandW}', reply_markup=keyboard)

    elif message.text == 'Изучить времена':
        keyboardTime = types.ReplyKeyboardMarkup(True)
        keyboardTime.add('Future perfect', 'Present perfect continuous')
        keyboardTime.add('Past perfect continuous', 'Future perfect continuous')
        keyboardTime.add('Present indefinite', 'Past indefinite')
        keyboardTime.add('Future indefinite', 'Present continuous')
        keyboardTime.add('Past continuous', 'Future continuous')
        bot.send_message(message.chat.id, 'Выберите какое время хотите щас изучить.', reply_markup=keyboardTime)

    elif message.text == 'Future perfect':
        bot.send_message(message.chat.id, f'{futurePerfect[1][0]} - {futurePerfect[1][1]}\n\nФормула: \n {futurePerfect[2]}\n\nОписание: \n {futurePerfect[3]}\n\nПример использования: \n {futurePerfect[4]}', reply_markup=keyboard)
    elif message.text == 'Present perfect continuous':
        bot.send_message(message.chat.id, f'{presentPerfectContinous[1][0]} - {presentPerfectContinous[1][1]}\n\nФормула: \n {presentPerfectContinous[2]}\n\nОписание: \n {presentPerfectContinous[3]}\n\nПример использования: \n {presentPerfectContinous[4]}', reply_markup=keyboard)
    elif message.text == 'Past perfect continuous':
        bot.send_message(message.chat.id, f'{pastPerfectContinuous[1][0]} - {pastPerfectContinuous[1][1]}\n\nФормула: \n {pastPerfectContinuous[2]}\n\nОписание: \n {pastPerfectContinuous[3]}\n\nПример использования: \n {pastPerfectContinuous[4]}', reply_markup=keyboard)
    elif message.text == 'Future perfect continuous':
        bot.send_message(message.chat.id, f'{futurePerfectContinuous[1][0]} - {futurePerfectContinuous[1][1]}\n\nФормула: \n {futurePerfectContinuous[2]}\n\nОписание: \n {futurePerfectContinuous[3]}\n\nПример использования: \n {futurePerfectContinuous[4]}', reply_markup=keyboard)
    elif message.text == 'Present indefinite':
        bot.send_message(message.chat.id, f'{presentIndefinite[1][0]} - {presentIndefinite[1][1]}\n\nФормула: \n {presentIndefinite[2]}\n\nОписание: \n {presentIndefinite[3]}\n\nПример использования: \n {presentIndefinite[4]}', reply_markup=keyboard)
    elif message.text == 'Past indefinite':
        bot.send_message(message.chat.id, f'{pastIndefinite[1][0]} - {pastIndefinite[1][1]}\n\nФормула: \n {pastIndefinite[2]}\n\nОписание: \n {pastIndefinite[3]}\n\nПример использования: \n {pastIndefinite[4]}', reply_markup=keyboard)
    elif message.text == 'Future indefinite':
        bot.send_message(message.chat.id, f'{futureIndefinite[1][0]} - {futureIndefinite[1][1]}\n\nФормула: \n {futureIndefinite[2]}\n\nОписание: \n {futureIndefinite[3]}\n\nПример использования: \n {futureIndefinite[4]}', reply_markup=keyboard)
    elif message.text == 'Present continuous':
        bot.send_message(message.chat.id, f'{presentContinous[1][0]} - {presentContinous[1][1]}\n\nФормула: \n {presentContinous[2]}\n\nОписание: \n {presentContinous[3]}\n\nПример использования: \n {presentContinous[4]}', reply_markup=keyboard)
    elif message.text == 'Past continuous':
        bot.send_message(message.chat.id, f'{pastContinous[1][0]} - {pastContinous[1][1]}\n\nФормула: \n {pastContinous[2]}\n\nОписание: \n {pastContinous[3]}\n\nПример использования: \n {pastContinous[4]}', reply_markup=keyboard)
    elif message.text == 'Future continuous':
        bot.send_message(message.chat.id, f'{futureContinous[1][0]} - {futureContinous[1][1]}\n\nФормула: \n {futureContinous[2]}\n\nОписание: \n {futureContinous[3]}\n\nПример использования: \n {futureContinous[4]}', reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, f'Привет! {message.from_user.last_name} {message.from_user.first_name}')

if __name__ == '__main__':
    bot.polling(none_stop = True)