from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ["HERMES_API_KEY"],
    base_url="https://inference-api.nousresearch.com/v1"
)

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

    msg = data.get("message") or data.get("business_message")

    if msg:
        chat_id = msg["chat"]["id"]
        connection_id = msg.get("business_connection_id")

        text = msg.get("text", "User sent non-text message")

        response = client.chat.completions.create(
            model="Hermes-4-70B",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content

        send_message(chat_id, answer, connection_id)

    return "ok"


app.run(host="0.0.0.0", port=8080)
