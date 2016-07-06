import const


from flask import Flask, request, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

import main_work

app = Flask(__name__)
kik = KikApi(const.bot_name, const.bot_api_key)

kik.set_configuration(Configuration(webhook= const.bot_server + 'incoming'))

@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'),  request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])



    for message in messages:
        if isinstance(message, TextMessage):
            main_work.func(message, TextMessage, kik)

            '''kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])'''



    return Response(status=200)


if __name__ == "__main__":
    app.run(port=8045, debug=True)