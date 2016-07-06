import telebot
import const
import ab
import requests


def CheckResponse(json):
    if json.status_code == 404:
        return False
    else:
        return True

bot = telebot.TeleBot(const.token)

@bot.message_handler(commands=['auth'])
def handle_command(message):
    print("auth")
    mcid = str(message.chat.id)
    if mcid in ab.users:
        if mcid in ab.state:
            del ab.state[mcid]
        bot.send_message(message.chat.id, "You are authorized already!")
    else:
        ab.state[mcid] = "auth"
        bot.send_message(message.chat.id, "What's your secret key?")

@bot.message_handler(commands=['help'])
def handle_command(message):
    bot.send_message(message.chat.id, "/auth - аутентификация по секретному ключу\n/list - получить нумерованный список заметок\n/delete - удалить заметку\n/add - добавить заметку\n/help - справочник")

@bot.message_handler(commands=['add'])
def handle_command(message):
    print("add")
    mcid = str(message.chat.id)
    if mcid in ab.users:
        if mcid in ab.state:
            del ab.state[mcid]
        ab.state[mcid] = "add"
        bot.send_message(message.chat.id, "Enter title")
    else:
        bot.send_message(message.chat.id, "You're not authorized yet!")

@bot.message_handler(commands=['delete'])
def handle_command(message):
    print("delete")
    mcid = str(message.chat.id)
    if mcid in ab.users:
        if mcid in ab.state:
            del ab.state[mcid]
        ab.state[mcid] = "delete"
        bot.send_message(message.chat.id, "Enter post id you wanna delete")
    else:
        bot.send_message(message.chat.id, "You're not authorized yet!")


@bot.message_handler(commands=['list'])
def handle_command(message):
    print("list")
    mcid = str(message.chat.id)
    if mcid in ab.users:
        if mcid in ab.state:
            del ab.state[mcid]

        url = const.django_server + "api/{}/list".format(ab.users[mcid])
        json = requests.get(url)

        if not CheckResponse(json):
            bot.send_message(message.chat.id, "Server doesn't response!")
            if mcid in ab.state:
                del ab.state[mcid]
            return

        msg = json.json()  # decode
        if msg['result'] != "ok":
            bot.send_message(message.chat.id, msg['result'])
        else:
            bot.send_message(message.chat.id, "Node List:")
            for item in msg['list']:
                msj = "{}. {}\n{}".format(str(item['id']), item['title'], item['text'])
                bot.send_message(message.chat.id, msj)
    else:
        bot.send_message(message.chat.id, "You're not authorized yet!")


@bot.message_handler(content_types=['text'])
def handle_command(message):
    print("text")
    mcid = str(message.chat.id)
    if not mcid in ab.state:
        return
    if ab.state[mcid] == "auth":
        url = const.django_server + "api/auth/{}".format(message.text)
        print(url)
        json = requests.get(url)  # get json answer

        if not CheckResponse(json):
            bot.send_message(message.chat.id, "Server doesn't response!")
            if mcid in ab.state:
                del ab.state[mcid]
            return

        msg = json.json()  # decode
        del ab.state[mcid]  # delete chat status

        if msg['is_auth'] == True:
            ab.users[mcid] = message.text
            bot.send_message(message.chat.id, "Successful authorization")
        else:
            bot.send_message(message.chat.id, "Not authorized")

    elif ab.state[mcid] == "delete":
        if message.text.isdigit():
            url = const.django_server + "api/{}/delete/{}".format(ab.users[mcid], message.text)
            print(url)
            json = requests.get(url)  # get json answer

            if not CheckResponse(json):
                bot.send_message(message.chat.id, "Server doesn't response!")
                if mcid in ab.state:
                    del ab.state[mcid]
                return

            msg = json.json()  # decode
            del ab.state[mcid]  # delete chat status
            bot.send_message(message.chat.id, msg['result'])
        else:
            del ab.state[mcid]
            bot.send_message(message.chat.id, "Incorrect query")

    elif ab.state[mcid] == "add":
        ab.state[mcid] = "title: {}".format(message.text)
        bot.send_message(message.chat.id, "Enter text")
    elif ab.state[mcid].startswith('title:') is True:
        url = const.django_server + "api/{}/add/{}/{}".format(ab.users[mcid], ab.state[mcid][7:], message.text)
        json = requests.get(url)

        if not CheckResponse(json):
            bot.send_message(message.chat.id, "Server doesn't response!")
            if mcid in ab.state:
                del ab.state[mcid]
            return

        msg = json.json()  # decode
        del ab.state[mcid]
        bot.send_message(message.chat.id, msg['result'])


bot.polling(none_stop=True, interval=0)

