import os
import re
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, request, Response, jsonify
from telegram import Bot
from telegram import InputFile as FSInputFile
from telegram.ext import Dispatcher, Update
from telegram.ext import CommandHandler, MessageHandler, Filters

# Получаем токен из переменных окружения
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("Bot token is not set in environment variables!")

# Создаем Flask приложение
app = Flask(__name__)

def parse_message(message):
    """ Парсим сообщение от Telegram API """
    print("message -->", message)

    if "message" not in message or "text" not in message["message"]:
        return None, None  # Если нет текста, пропускаем

    chat_id = message["message"]["chat"]["id"]
    txt = message["message"]["text"]

    print("chat_id -->", chat_id)
    print("txt -->", txt)

    return chat_id, txt

@app.route('/setwebhook', methods=['POST', 'GET'])
def setwebhook():
    if request.method == 'POST':
        webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={os.environ.get('VERCEL_URL')}/webhook"
        response = requests.get(webhook_url)
        
        if response.status_code == 200:
            return "Webhook successfully set", 200
        else:
            return f"Error setting webhook: {response.text}", response.status_code
    else:
        return "Vercel URL not found", 400



def tel_send_message(chat_id, text):
    """ Отправка сообщения в Telegram """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Ошибка отправки сообщения:", response.text)

    return response

# Обработчик команды /start
@app.route('/webhook', methods=['POST'])
def webhook():
    msg = request.get_json()

    chat_id, txt = parse_message(msg)
    if chat_id is None or txt is None:
        return jsonify({"status": "ignored"}), 200

    if txt.lower() == "/start":
        tel_send_message(chat_id, "Привет! Напиши /analyze, чтобы выбрать монету для анализа.")
    elif txt.lower() == "/analyze":
        tel_send_message(chat_id, "Выберите монету для анализа. Например, BTC-USD или ETH-USD:")  
    elif re.match(r'^[A-Za-z\-]+$', txt):  # Проверка на валидность монеты
        choose_coin(chat_id, txt.strip().upper())
    elif re.match(r'\d{4}-\d{2}-\d{2}', txt):  # Проверка на правильность формата даты
        analyze_btc_with_date(chat_id, txt.strip())

    return Response('ok', status=200)


# Функции обработки команд

def parse_message(msg):
    """ Извлекаем chat_id и текст сообщения """
    try:
        chat_id = msg['message']['chat']['id']
        text = msg['message']['get']('text')
        return chat_id, text
    except KeyError:
        return None, None


def tel_send_message(chat_id, text):
    """ Отправка сообщения в Telegram """
    bot.send_message(chat_id=chat_id, text=text)


def choose_coin(chat_id, coin):
    """ Обработка ввода монеты """
    valid_coins = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD']  # Доступные монеты

    if coin in valid_coins:
        user_coin_choice[chat_id] = coin
        tel_send_message(chat_id, f"Вы выбрали {coin}. Теперь введите дату начала периода в формате YYYY-MM-DD:")
    else:
        tel_send_message(chat_id, "Монета не найдена. Пожалуйста, выберите одну из доступных: BTC-USD, ETH-USD, LTC-USD, XRP-USD.")


def analyze_btc_with_date(chat_id, start_date):
    """ Обработка ввода даты и запуск анализа """
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        tel_send_message(chat_id, "Дата введена неверно. Пожалуйста, используйте формат YYYY-MM-DD.")
        return

    coin = user_coin_choice.get(chat_id)
    if not coin:
        tel_send_message(chat_id, "Сначала выберите монету с помощью команды /analyze.")
        return

    end_date = datetime.now().strftime('%Y-%m-%d')
    tel_send_message(chat_id, f"Анализирую {coin} с {start_date} по {end_date}...")

    # Загрузка данных о выбранной монете
    data = yf.download(coin, start=start_date, end=end_date)

    # Расчет MACD
    fast_ema = data['Close'].ewm(span=12, min_periods=1).mean()
    slow_ema = data['Close'].ewm(span=26, min_periods=1).mean()
    data['MACD'] = fast_ema - slow_ema
    data['Signal'] = data['MACD'].ewm(span=9, min_periods=1).mean()

    # Генерация сигналов
    data['Buy_Signal'] = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1))
    data['Sell_Signal'] = (data['MACD'] < data['Signal']) & (data['MACD'].shift(1) >= data['Signal'].shift(1))

    # Расчет RSI
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    average_gain = gain.rolling(window=14).mean()
    average_loss = loss.rolling(window=14).mean()
    rs = average_gain / average_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Расчет волатильности
    data['Volatility'] = data['Close'].rolling(window=14).std() * (252 ** 0.5)

    # Визуализация
    plt.figure(figsize=(12, 12))

    # График MACD
    plt.subplot(4, 1, 1)
    plt.plot(data['MACD'], label='MACD', color='blue', alpha=0.7)
    plt.plot(data['Signal'], label='Signal', color='orange', alpha=0.7)
    plt.fill_between(data.index, data['MACD'], data['Signal'], where=(data['MACD'] > data['Signal']), color='green', alpha=0.3)
    plt.fill_between(data.index, data['MACD'], data['Signal'], where=(data['MACD'] < data['Signal']), color='red', alpha=0.3)
    plt.title('MACD и Сигнальная Линия')
    plt.legend()

    # Сигналы на покупку и продажу
    plt.subplot(4, 1, 2)
    plt.plot(data['Close'], label='Цена', color='gray', alpha=0.5)
    plt.scatter(data[data['Buy_Signal']].index, data[data['Buy_Signal']]['Close'], marker='^', color='g', label='Buy Signal', s=100)
    plt.scatter(data[data['Sell_Signal']].index, data[data['Sell_Signal']]['Close'], marker='v', color='r', label='Sell Signal', s=100)
    plt.title('Сигналы на покупку и продажу')
    plt.legend()

    # RSI
    plt.subplot(4, 1, 3)
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    plt.fill_between(data.index, 30, 70, where=(data['RSI'] >= 30) & (data['RSI'] <= 70), color='yellow', alpha=0.2)
    plt.title('RSI (Индекс относительной силы)')
    plt.legend()

    # Волатильность
    plt.subplot(4, 1, 4)
    plt.plot(data['Volatility'], label='Volatility', color='red')
    plt.title('Годовая Волатильность')
    plt.legend()

    plt.tight_layout()

    # Сохранение изображения
    img_path = "coin_analysis.png"
    plt.savefig(img_path)
    plt.close()

    # Отправка изображения в Telegram
    tel_send_message(chat_id, f"Анализ {coin} с {start_date} по {end_date}...")
    bot.send_photo(chat_id=chat_id, photo=FSInputFile(img_path))

@app.route("/", methods=['GET'])
def index():
    return "<h1>Telegram Bot Webhook is Running</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

