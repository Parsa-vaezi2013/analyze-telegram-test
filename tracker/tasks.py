import threading
import time
from .models import Profile
from telegram_bot.bot import send_alert
import requests
from django.conf import settings  # اگه از settings.py توکن رو بگیری

BOT_TOKEN = '8171301737:AAGUb8GQ6M8TqIvOFARMpCJjVIz7hnhry00'

def get_follower_count(channel_username):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMembersCount?chat_id=@{channel_username}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("result", 0)
    except Exception as e:
        print("خطا در دریافت تعداد اعضا:", e)
        return 0


def check_falowers():
    while True:
        print("1000 years later")
        for profile in Profile.objects.all():
            new_count = get_follower_count(profile.username)
            print (f"{profile.username}:{profile.fallower_count} -> {new_count}")
            if profile.fallower_count <profile.alert_threshold <= new_count:
                send_alert(profile.telegram_chat_id, f"🎉🎉🎉 {profile.username} به {new_count} دنبال کننده رسید")
            profile.fallower_count = new_count
            profile.save()
        time.sleep(60)

threading.Thread(target=check_falowers, deamom= True).start