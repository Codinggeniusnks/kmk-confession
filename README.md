# KMK CONFESSION

A Telegram bot that accepts confessions in a private chat and publishes their text to a configured Telegram group or channel.

## Setup

Requires Python 3.11. Install dependencies with `pip install -r requirements.txt`, set `BOT_TOKEN` and `CONFESSION_CHANNEL` in the process environment, then run `python main.py`.

Create a bot with Telegram's official BotFather and give it permission to post to the destination. Set `CONFESSION_CHANNEL` to your destination's chat ID or public username. Never commit the token or private chat IDs. `.env.example` is a blank template; this project does not automatically load `.env` files.

For Render, import this repository and configure the two environment variables as private settings. Run only one polling instance per token. The HTTP route is a basic health endpoint; the included Flask development server should be replaced with an appropriate production server for production use.

## Privacy and limits

This public version removes sender-identity logging and admin identity notifications from the original project. It publishes text as a new message rather than forwarding the original, and accepts only private-chat text messages. It keeps an in-memory timestamp per sender for a 30-second posting cooldown, which resets on restart. It does not persist confession text or user profiles to a database.

Anonymous means the bot does not attach the sender's identity to the published message. Telegram and the running bot still process account identifiers and message contents; this is not end-to-end anonymous messaging. Confessions can identify their author through their own wording. Posts are published immediately without human moderation, so operators must establish moderation and abuse-handling procedures before public use. The cooldown is per account, not a complete spam defense.

The repository contains no production bot token, private administrator ID, confession history, or user database. Store credentials only in the hosting environment. If a token was previously shared or stored in an unsafe place, replace it through BotFather before deployment.

Publishing this repository does not update an existing deployed bot or remove its old hosting logs.
