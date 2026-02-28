from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# ключи из Railway
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]


def send_message(chat_id, text, connection_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if connection_id:
        data["business_connection_id"] = connection_id

    requests.post(url, json=data)


@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("DATA:", data)

    msg = data.get("message") or data.get("business_message")

    if msg:
        chat_id = msg["chat"]["id"]
        connection_id = msg.get("business_connection_id")

        if "text" in msg:
            text = msg["text"]

        elif "voice" in msg:
            text = "User sent a voice message."

        elif "sticker" in msg:
            text = "User sent a sticker."

        else:
            text = "User sent something else."

        print("TEXT:", text)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ]
        )

        answer = response.choices[0].message.content
        print("ANSWER:", answer)

        send_message(chat_id, answer, connection_id)

    return "ok"


app.run(host="0.0.0.0", port=8080)
