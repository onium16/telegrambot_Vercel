import os
import requests
from flask import Flask, Response, request


TOKEN = os.environ.get('TOKEN')

app = Flask(__name__)


def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
    r = requests.post(url,json=payload)
    print(r)
    return r
 
@app.route('/webhook', methods=['GET', 'POST'])
def check_req():
    if request.method == 'POST':
        msg = request.get_json()
        
        chat_id,txt = parse_message(msg)
        if txt == "hi":
            tel_send_message(chat_id,"Hello!!")

        else:
            tel_send_message(chat_id,'from webhook')
       
        return Response('ok', status=200)
    else:
        return "<h1>Get 'GET' received!</h1>"
 

@app.route("/", methods=['GET'])
def index():
    return "<h1>Welcome to telegrambot!</h1>"
 

@app.route("/about", methods=['GET'])
def get_about():
    return "<h1>About to telegrambot!</h1>"
