# Chat Counter Bot

A small Telegram bot that replies to every incoming message with a per-chat counter. Counts are stored in SQLite and survive restarts.

## Run on Windows

1. Install Python 3.10 or newer from https://www.python.org/downloads/ and enable the Python launcher if the installer offers it.
2. Download this repository using **Code → Download ZIP**, then extract the ZIP.
3. Double-click `start.bat` in the extracted folder.
4. At the hidden `BotFather token` prompt, paste your current bot token and press Enter. The token will not appear as you type.

Keep the bot window open while you want the bot to respond. Press `Ctrl+C` in that window to stop it. Counts are saved locally in `counters.sqlite3`.

In group chats, Telegram bots may only receive commands or messages that mention them by default. To count every group message, open BotFather, use `/setprivacy`, select the bot, and choose **Disable**. Then remove and add the bot to the group again.
