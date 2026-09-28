# Chat Counter Bot

A small Telegram bot that replies to every incoming message with a per-chat counter. Counts are stored in SQLite and survive restarts.

## Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder and enter the token privately when prompted:

   ```powershell
   $secureToken = Read-Host "BotFather token" -AsSecureString
   $env:BOT_TOKEN = [System.Net.NetworkCredential]::new("", $secureToken).Password
   Remove-Variable secureToken
   python bot.py
   ```

3. Send a message to the bot. Stop it with `Ctrl+C`.

The token is read from the environment and must never be committed to GitHub. The SQLite database is created locally as `counters.sqlite3`.

In group chats, Telegram bots may only receive commands or messages that mention them by default. To count every group message, open BotFather, use `/setprivacy`, select the bot, and choose **Disable**. Then remove and add the bot to the group again.
