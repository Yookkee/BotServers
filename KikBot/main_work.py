import requests

import ab
import const

def func(message, TextMessage, kik):

    id = str(message.chat_id)
    if not id in ab.state:  # base_abstate
        if (message.body == 'auth'):
            if id in ab.user:
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body='You authorized'
                    )
                ])
            else:
                ab.state[id] = 'auth'
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="What's your secret key"
                    )
                ])
        elif message.body == "list":
            if id in ab.user:
                url = const.dj_server + "api/{}/list".format(ab.user[id])
                json = requests.get(url)
                if json.status_code == 404:
                    del ab.state[id]
                    kik.send_messages([
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body="Server is dead"
                        )
                    ])
                msg = json.json()
                if msg['result'] != "ok":
                    kik.send_messages([
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body=msg['result']
                        )
                    ])
                else:
                    kik.send_messages([
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body="Node List:"
                        )
                    ])
                    for item in msg['list']:
                        msj = "{}. {}\n{}".format(str(item['id']), item['title'], item['text'])
                        kik.send_messages([
                            TextMessage(
                                to=message.from_user,
                                chat_id=message.chat_id,
                                body=msj
                            )
                        ])
            else:
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="You're not authorized yet!"
                    )
                ])

        elif message.body == 'add':
            if id in ab.user:
                ab.state[id] = 'add'
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Enter title"
                    )
                ])

            else:
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="You're not authorized yet!"
                    )
                ])


        elif message.body == 'delete':
            if id in ab.user:
                ab.state[id] = 'delete'
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Enter node id you wanna delete"
                    )
                ])
            else:
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="You're not authorized yet!"
                    )
                ])

    elif ab.state[id] == 'delete':
        if message.body.isdigit():
            url = const.dj_server + "api/{}/delete/{}".format(ab.user[id], message.body)
            json = requests.get(url)  # get json answer
            if json.status_code == 404:
                del ab.state[id]
                kik.send_messages([
                    TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Server is dead"
                    )
                ])
            msg = json.json()  # decode
            del ab.state[id]  # delete chat status
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=msg['result']
                )
            ])
        else:
            del ab.state[id]
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Incorrect query"
                )
            ])





    elif ab.state[id] == "auth":
        url = const.dj_server + "api/auth/{}".format(message.body)
        json = requests.get(url)
        if json.status_code == 404:
            del ab.state[id]
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Server is dead"
                )
            ])
        msg = json.json()
        if msg['is_auth'] == True:
            ab.user[id] = message.body
            del ab.state[id]
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Successful authorization"
                )
            ])
        else:
            del ab.state[id]
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Not authorized"
                )
            ])


    elif ab.state[id] == 'add':
        ab.state[id] = "title: {}".format(message.body)
        kik.send_messages([
            TextMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                body="Enter text"
            )
        ])

    elif ab.state[id].startswith('title:') is True:
        url = const.dj_server + "api/{}/add/{}/{}".format(ab.user[id], ab.state[id][7:], message.body)
        json = requests.get(url)
        if json.status_code == 404:
            del ab.state[id]
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Server is dead"
                )
            ])
        msg = json.json()  # decode
        del ab.state[id]
        kik.send_messages([
            TextMessage(
                to=message.from_user,
                chat_id=message.chat_id,
                body=msg['result']
            )
        ])



    return