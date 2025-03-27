# Telegrambot with Flask and deployed on Vercel (webhook)

This is a sample project to create a static webhook for a Telegram bot using Flask and deploying it on Vercel to receive messages from the bot.

## How it Works

Let me explain step by step what we're doing here:

**Flask and Webhook for Telegram Bot:** We use Flask to create a simple web application that will serve as the webhook. A webhook is an HTTP method through which Telegram will send updates about new messages.

**Deployment on Vercel:** Vercel is a platform for automatic deployment of server-side applications (such as Flask). We can use Vercel to host our application, which will accept requests from Telegram.

**Deployment Process:** We deploy our Flask application on Vercel, and Vercel automatically generates a public URL (e.g., https\://<project-name>.vercel.app), which will be used as the webhook URL for Telegram.

## Cloning and Setting Up Locally

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/onium16/telegrambot_Vercel
   ```
2. Navigate into the project directory:
   ```bash
   cd telegrambot_Vercel
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.

## Register Your Application in Vercel

You can use [Vercel CLI](https://vercel.com/cli) to register your application in Vercel.

AND in [https://vercel.com/](https://vercel.com/)-projects/telegram-vercel-bot-2-0/settings/environment-variables
add `TOKEN` for Telegram Bot
AND RELOAD VERCEL container.

## Register webhook in Telegram

```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://telegram-vercel-bot-2-0-nvqrweklj-onium16s-projects.vercel.app/webhook"
```

Response:

```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

## Verify Webhook Status

To check if the webhook is correctly set:

```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

Expected response should include:

```json
{"ok":true, "result": {"url": "https://telegram-vercel-bot-2-0-nvqrweklj-onium16s-projects.vercel.app/webhook"}}
```

## Debugging & Troubleshooting

### 1. Check Vercel Logs

```bash
vercel logs telegram-vercel-bot-2-0
```

### 2. Test Webhook Locally

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message": {"chat": {"id": 123456}, "text": "hi"}}' \
http://127.0.0.1:5000/webhook
```

Expected response: `Hello!!`

If the bot is not responding, ensure your `TOKEN` is correctly set in the Vercel environment and that Flask receives Telegram requests properly.

## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com?utm_source=github\&utm_medium=readme\&utm_campaign=vercel-examples):



## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask&demo-title=Flask%20%2B%20Vercel&demo-description=Use%20Flask%202%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)
