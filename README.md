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

## Get a token from @BotFather

To get a token from @BotFather, follow these steps:

1. Create a new bot using @BotFather.
2. Get the token from the bot's settings.

## Deploying to Vercel

To deploy the Flask application to Vercel, follow these steps:

1. Create a new Vercel project.
2. Deploy the Flask application to Vercel.
3. Set the `TOKEN` environment variable in Vercel.
4. Deploy the Vercel project.


## Deploying to Vercel (First method with Vercel CLI)

To deploy the project, use the following commands:

1. Install Vercel CLI globally:
   ```bash
   npm i -g vercel
   ```
2. Deploy in testing mode:
   ```bash
   vercel
   ```
3. Deploy in production mode:
   ```bash
   vercel --prod
   ```

After executing `vercel --prod`, Vercel will generate a permanent URL for the Telegram webhook.

Your Flask application is now available at `http://localhost:3000`.

## Register Your Application in Vercel

You can use [Vercel CLI](https://vercel.com/cli) to register your application in Vercel.

AND in [https://vercel.com/](https://vercel.com/)-projects/telegram-image-reposter-2-0/settings/environment-variables add `TOKEN` for Telegram Bot AND RELOAD VERCEL container.


## Alternative: Deploy via GitHub Integration

1. Go to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New Project"**.
3. Select your GitHub repository.
4. Follow the instructions to complete the setup.

Now, every time you push changes to GitHub, Vercel will automatically redeploy the project.

## Register webhook in Telegram

```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<app_name>.vercel.app/webhook"
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
{"ok":true, "result": {"url": "https://<app_name>.vercel.app/webhook"}}
```


## Debugging & Troubleshooting

### 1. Check Vercel Logs

```bash
vercel logs telegram-image-reposter-2-0
```

### 2. Test Webhook Locally

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message": {"chat": {"id": 123456}, "text": "hi"}}' \
ttps://<app_name>.vercel.app/webhook
```

Expected response: `Hello!!`

If the bot is not responding, ensure your `TOKEN` is correctly set in the Vercel environment and that Flask receives Telegram requests properly.

## Remove Old Deployments

To remove old deployments and keep only the latest one:

1. List all deployments:
   ```bash
   vercel list telegram-image-reposter-2-0
   ```
2. Identify the outdated deployments and delete them:
   ```bash
   vercel remove <DEPLOYMENT_ID>
   ```
   Replace `<DEPLOYMENT_ID>` with the ID of the deployment you want to remove.
3. Confirm the deletion by listing deployments again:
   ```bash
   vercel list telegram-image-reposter-2-0
   ```

## One-Click Deploy

Deploy the example using [Vercel](https://vercel.com)
