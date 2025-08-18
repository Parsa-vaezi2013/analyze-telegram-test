from celery import shared_task
from .models import Profile
from .utils import get_follower_count
from telegram_bot.bot import send_alert

@shared_task
def check_followers():
    for profile in Profile.objects.all():
        new_count = get_follower_count(profile.username)
        if profile.follower_count < profile.alert_threshold <= new_count:
            send_alert(profile.telegram_chat_id, f"🎉 {profile.username} به {new_count} عضو رسید!")
        profile.follower_count = new_count
        profile.save()
