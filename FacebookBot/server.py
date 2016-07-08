import json

from flask import Flask, request
import requests
import main_work

app = Flask(__name__)

ACCESS_TOKEN = "EAAYkzpBatckBAHCQywlQqhZALcUxg7K1rSwiqWYFLjabcMSRifWDnK7GCZAxtJfVqZCyjwD1TUld60XwfdAdMufZCrmeZCL8gGzu4YhjOCGd18VsHTemKy7ehd0kqL4zfMzyXSRTZBE7mIgngAkjF0HTonkZCYSUON5qoP25aZBMaQZDZD"
VERIFY_TOKEN = "frgsrdfghjmdf"

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
    if r.status_code != 200:
        print(r)

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    message_text = messaging_event["message"]["text"]  # the message's text

                    main_work.main_work(sender_id, message_text)

                    '''url = "http://bd8f77ad.ngrok.io/api/auth/meow"
                    jss = requests.get(url)
                    msg = jss.json()
                    if msg['is_auth'] == True:
                        reply(sender_id, "true")
                    else:
                        reply(sender_id, "else")'''

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)