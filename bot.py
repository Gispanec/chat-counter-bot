import json
import os
import sqlite3
import time
import urllib.error
import urllib.request


TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "counters.sqlite3")


def telegram_request(method: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        result = json.load(response)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error in {method}: {result}")
    return result["result"]


def next_count(connection: sqlite3.Connection, chat_id: int) -> int:
    with connection:
        row = connection.execute(
            "SELECT count FROM chat_counters WHERE chat_id = ?", (chat_id,)
        ).fetchone()
        count = (row[0] if row else 0) + 1
        connection.execute(
            """
            INSERT INTO chat_counters (chat_id, count)
            VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET count = excluded.count
            """,
            (chat_id, count),
        )
    return count


def main() -> None:
    if not TOKEN:
        raise SystemExit("Set the BOT_TOKEN environment variable before starting.")

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_counters (
            chat_id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL
        )
        """
    )

    print("Bot is running. Press Ctrl+C to stop.")
    offset = None
    while True:
        try:
            payload = {"timeout": 30}
            if offset is not None:
                payload["offset"] = offset
            updates = telegram_request("getUpdates", payload)

            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message")
                if message is None:
                    continue

                chat_id = message["chat"]["id"]
                count = next_count(connection, chat_id)
                telegram_request("sendMessage", {"chat_id": chat_id, "text": str(count)})
                print(f"Chat {chat_id}: sent {count}")

        except (urllib.error.URLError, TimeoutError, RuntimeError) as error:
            print(f"Telegram request failed: {error}. Retrying in 5 seconds.")
            time.sleep(5)


if __name__ == "__main__":
    main()
