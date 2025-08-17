# tracker/tasks.py
import requests
from celery import shared_task
from django.conf import settings
from .models import Profile

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHANNEL_ID = settings.TELEGRAM_CHANNEL_ID  # مثل -1002835752715

@shared_task
def check_followers():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMemberCount"
        params = {"chat_id": CHANNEL_ID}
        response = requests.get(url, params=params).json()

        if not response.get("ok"):
            print("❌ Telegram API Error:", response)
            return

        member_count = response["result"]
        print(f"📊 Current members: {member_count}")

        # از جدول Profile فقط اولین رکورد رو می‌گیریم (یا میشه چندتا باشه)
        profile, created = Profile.objects.get_or_create(username="MyChannel")
        
        if created:
            profile.follower_count = member_count
            profile.save()
            print("ℹ️ Profile created with initial count.")
            return

        # اگر تعداد افزایش پیدا کرد
        if member_count > profile.follower_count:
            new_users = member_count - profile.follower_count
            welcome_text = f"🎉 خوش اومدید {new_users} عضو جدید!"
            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            send_params = {"chat_id": CHANNEL_ID, "text": welcome_text}
            send_resp = requests.get(send_url, params=send_params).json()
            print("📨 Welcome message sent:", send_resp)

        profile.follower_count = member_count
        profile.save()

    except Exception as e:
        print("🚨 Error in check_followers:", e)
