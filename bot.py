# !/usr/bin/python3

import os
import sys
import config
import telebot

bot = telebot.TeleBot(config.token)
COMMAND = 'psql -U postgres -d postgres -c '


def incriment_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"UPDATE users_chsv SET chsv = chsv + 1 WHERE user_name = '+str_username+'"'
    read = os.popen(COMMAND + sql_command).read()
    print("incriment_chsv - " + str(read))

def get_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"SELECT "chsv" FROM users_chsv WHERE user_name = '+str_username+'"'
    read = os.popen(COMMAND + sql_command).read()
    list_read = read.split()
    print("get_chsv - " + str(read))
    return list_read[2]


def add_user(username,id):
    str_username = "'" + username + "'"
    sql_command = '"INSERT INTO users_chsv (user_name,user_id) VALUES ('+str_username+','+str(id)+')"'
    read = os.popen(COMMAND + sql_command).read()
    print("add_user - " + str(read))


def decrement_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"UPDATE users_chsv SET chsv = chsv - 1 WHERE user_name = ' + str_username + '"'
    read = os.popen(COMMAND + sql_command).read()
    print("decrement_chsv - " + str(read))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    if("Одобряю" in message.text and message.reply_to_message != None):
        good_user = message.reply_to_message.from_user.username
        if(if_user_exist(good_user)):
            incriment_chsv(good_user)
            bot.send_message(message.chat.id, "ЧСВ пользователя @"+good_user + " увеличилось и равно " + str(get_chsv(good_user)))
        else:
            add_user(good_user,message.reply_to_message.from_user.id)
            incriment_chsv(good_user)
            bot.send_message(message.chat.id,
                             "С почином @" + good_user + ", вас одобрили впервые! чсв равно " + str(get_chsv(good_user)))
    elif("Осуждаю" in message.text and message.reply_to_message != None):
        bad_user = message.reply_to_message.from_user.username
        if (if_user_exist(bad_user)):
            decrement_chsv(bad_user)
            bot.send_message(message.chat.id,
                             "ЧСВ пользователя @" + bad_user + " уменьшилось и равно " + str(get_chsv(bad_user)))
        else:
            add_user(bad_user, message.reply_to_message.from_user.id)
            decrement_chsv(bad_user)
            bot.send_message(message.chat.id,
                             "Так себе начало @" + bad_user + ", вас осудили! чсв равно " + str(
                                 get_chsv(bad_user)))


def if_user_exist(username):
    sql_command = '"SELECT "user_name" FROM users_chsv"'
    read = os.popen(COMMAND + sql_command).read()
    print("if_user_exist - \n" + read)
    if(username in read):
        return True
    else:
        return False


if __name__ == '__main__':
     bot.infinity_polling()