import os
import requests
from dotenv import load_dotenv 
from flask import Flask, Response, render_template, request, jsonify


load_dotenv()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN is not set")

app = Flask(__name__)

# List to store received messages (for display on the page)
message_logs = []

def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
    r = requests.post(url, json=payload)
    return r

@app.route('/webhook', methods=['GET', 'POST'])
def check_req():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, txt = parse_message(msg)
        
        # Log the received message and response
        message_logs.append(f"Received: {txt} from Chat ID: {chat_id}")
        
        if txt == "hi":
            tel_send_message(chat_id, "Hello!!")
            message_logs.append(f"Sent: Hello!! to Chat ID: {chat_id}")
        else:
            tel_send_message(chat_id, 'from webhook')
            message_logs.append(f"Sent: from webhook to Chat ID: {chat_id}")
        
        return Response('ok', status=200)
    else:
        return render_template("webhook.html")  # You may need to create the webhook.html file.
 
@app.route("/", methods=['GET'])
def index():
    # Pass the logs to the index page
    return render_template("index.html", message_logs=message_logs)

@app.route("/logs", methods=["GET"])
def get_logs():
    # Return the message logs in JSON format
    return jsonify(message_logs)

@app.route("/about", methods=['GET'])
def get_about():
    return "<h1>About the Telegram bot!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
