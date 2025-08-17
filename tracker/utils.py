import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 

def get_follower_count(chat_id):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMemberCount"
    response = requests.get(url, params={"chat_id": chat_id})
    data = response.json()

    if data.get("ok"):
        return data["result"]  
    else:
        raise Exception(f"Telegram API Error: {data}")
