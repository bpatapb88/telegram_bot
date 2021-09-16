# !/usr/bin/python3
import json
import os
import telebot
import config

bot = telebot.TeleBot(config.token)
COMMAND = 'psql -U postgres -d postgres -c '


def incriment_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"UPDATE users_chsv SET chsv = chsv + 1 WHERE user_name = ' + str_username + '"'
    read = os.popen(COMMAND + sql_command).read()
    print("incriment_chsv - " + str(read))


def get_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"SELECT "chsv" FROM users_chsv WHERE user_name = ' + str_username + '"'
    read = os.popen(COMMAND + sql_command).read()
    list_read = read.split()
    print("get_chsv - " + str(read))
    return list_read[2]


def add_user(username, user_id):
    str_username = "'" + username + "'"
    sql_command = '"INSERT INTO users_chsv (user_name,user_id) VALUES (' + str_username + ',' + str(user_id) + ')"'
    read = os.popen(COMMAND + sql_command).read()
    print("add_user - " + str(read))


def decrement_chsv(username):
    str_username = "'" + username + "'"
    sql_command = '"UPDATE users_chsv SET chsv = chsv - 1 WHERE user_name = ' + str_username + '"'
    read = os.popen(COMMAND + sql_command).read()
    print("decrement_chsv - " + str(read))


@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
    new_user = message.new_chat_members[0].username
    welcome = "Добро пожаловать @" + new_user + " в флудчат группы stůl jako kachon! \n \nКоротко: тут ценится вежливость в интернет-общении, а на сходосах - открытость и инициативность. \n\nМы уважаем репутацию и конкретно в этом чате поощряем флуд. Работают команды одобряю/осуждаю и /report. В описании чата есть ссылки на Стул яко кахон в других соц сетях, подписывайся :) приятного общения и до встречи на ближайшем мероприятии!"
    bot.reply_to(message, welcome)


@bot.message_handler(content_types=["left_chat_member"])
def foo(message):
    bot.reply_to(message, "кто не с нами, тот под нами ))0)")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print(message)
    if message.json.get("entities") is not None and message.json["entities"][0]["type"] == "bot_command":
        # 399231972 - Sonia
        if message.reply_to_message is not None:
            bot.forward_message(399231972, message.chat.id, message.reply_to_message.id)
            bot.reply_to(message.reply_to_message, "Репорт отправлен админу, тікай з міста")
        else:
            bot.reply_to(message, "Какое сообщение репортите?")

        return

    if "Одобряю" in message.text and message.reply_to_message is not None:
        json_value = json.dumps(message.json)
        print(json_value)
        good_user = message.reply_to_message.from_user.username
        initiator = message.from_user.username

        if message.from_user.id == message.reply_to_message.from_user.id:
            bot.send_message(message.chat.id,
                             "Сам не похвалишь, никто не повалит, да @" + good_user + "?")
            return

        if if_user_exist(good_user):
            incriment_chsv(good_user)
            bot.send_message(message.chat.id,
                             "@" + good_user + ", ваше чсв повысил пользователь @" + initiator + ".\nНа данный момент Ваш уровень чсв " + str(
                                 get_chsv(good_user)))
        else:
            add_user(good_user, message.reply_to_message.from_user.id)
            incriment_chsv(good_user)
            bot.send_message(message.chat.id,
                             "С почином @" + good_user + ", первым вас одобрил @" + initiator + "! чсв равно " + str(
                                 get_chsv(good_user)))
    elif "Осуждаю" in message.text and message.reply_to_message is not None:
        bad_user = message.reply_to_message.from_user.username
        initiator = message.from_user.username
        if message.from_user.id == message.reply_to_message.from_user.id:
            bot.send_message(message.chat.id,
                             "Чтож ты так себя не любишь @" + bad_user + ", а?")
            return
        if if_user_exist(bad_user):
            decrement_chsv(bad_user)
            bot.send_message(message.chat.id,
                             "@" + bad_user + ", вас понизил пользователь @" + initiator + ".\nНа данный момент Ваш уровень чсв " + str(
                                 get_chsv(bad_user)))
        else:
            add_user(bad_user, message.reply_to_message.from_user.id)
            decrement_chsv(bad_user)
            bot.send_message(message.chat.id,
                             "Так себе начало @" + bad_user + ", вас осудил @" + initiator + "! ЧСВ = " + str(
                                 get_chsv(bad_user)))


def if_user_exist(username):
    sql_command = '"SELECT "user_name" FROM users_chsv"'
    read = os.popen(COMMAND + sql_command).read()
    print("if_user_exist - \n" + read)
    if username in read:
        return True
    else:
        return False


if __name__ == '__main__':
    bot.infinity_polling()
