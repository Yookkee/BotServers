import json
import ab
import requests
import const

ACCESS_TOKEN = "EAAYkzpBatckBAHCQywlQqhZALcUxg7K1rSwiqWYFLjabcMSRifWDnK7GCZAxtJfVqZCyjwD1TUld60XwfdAdMufZCrmeZCL8gGzu4YhjOCGd18VsHTemKy7ehd0kqL4zfMzyXSRTZBE7mIgngAkjF0HTonkZCYSUON5qoP25aZBMaQZDZD"

def reply(user_id, msg):
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": msg
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def main_work(id, text):
    if not id in ab.state:  # base_abstate
        if (text == 'auth'):
            if id in ab.user:
                reply(id, "You are authorized already")
            else:
                ab.state[id] = 'auth'
                reply(id, "What's your secret key")
        elif text == "list":
            if id in ab.user:
                url = const.dj_server + "api/{}/list".format(ab.user[id])
                json = requests.get(url)
                if json.status_code == 404:
                    del ab.state[id]
                    reply(id, "Server is dead")
                msg = json.json()
                if msg['result'] != "ok":
                    reply(id, msg['result'])
                else:
                    reply(id, "Node List:")
                    for item in msg['list']:
                        msj = "{}. {}\n{}".format(str(item['id']), item['title'], item['text'])
                        reply(id, msj)
            else:
                reply(id, "You're not authorized yet!")

        elif text == 'add':
            if id in ab.user:
                ab.state[id] = 'add'
                reply(id, "Enter title")

            else:
                reply(id, "You're not authorized yet!")


        elif text == 'delete':
            if id in ab.user:
                ab.state[id] = 'delete'
                reply(id, "Enter node id you wanna delete")
            else:
                reply(id, "You're not authorized yet!")

    elif ab.state[id] == 'delete':
        if text.isdigit():
            url = const.dj_server + "api/{}/delete/{}".format(ab.user[id], text)
            json = requests.get(url)  # get json answer
            if json.status_code == 404:
                del ab.state[id]
                reply(id, "Server is dead")
            msg = json.json()  # decode
            del ab.state[id]  # delete chat status
            reply(id, msg['result'])
        else:
            del ab.state[id]
            reply(id, "Incorrect query")





    elif ab.state[id] == "auth":
        url = const.dj_server + "api/auth/{}".format(text)
        json = requests.get(url)
        if json.status_code == 404:
            del ab.state[id]
            reply(id, "Server is dead")
        msg = json.json()
        if msg['is_auth'] == True:
            ab.user[id] = text
            del ab.state[id]
            reply(id, "Successful authorization")
        else:
            del ab.state[id]
            reply(id, "Not authorized")


    elif ab.state[id] == 'add':
        ab.state[id] = "title: {}".format(text)
        reply(id, "Enter text")

    elif ab.state[id].startswith('title:') is True:
        url = const.dj_server + "api/{}/add/{}/{}".format(ab.user[id], ab.state[id][7:], text)
        json = requests.get(url)
        if json.status_code == 404:
            del ab.state[id]
            reply(id, "Server is dead")
        msg = json.json()  # decode
        del ab.state[id]
        reply(id, msg['result'])

    return