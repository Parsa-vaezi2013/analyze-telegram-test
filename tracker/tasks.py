import threading
import time
from .models import Profile
from telegram_bot.bot import send_alert

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