from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["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"])
TELEGRAM_TOKEN = os.environ["8771274594:AAHIp3IvuFPKqJ0VY-cvVnHfehcGlT1mZ_k"]

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{8771274594:AAHIp3IvuFPKqJ0VY-cvVnHfehcGlT1mZ_k}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )

        answer = response.choices[0].message.content
        send_message(chat_id, answer)

    return "ok"

app.run(host="0.0.0.0", port=8080)
