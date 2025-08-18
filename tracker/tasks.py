import os
import httpx
from celery import shared_task
from .models import Profile

BOT_TOKEN = os.getenv("BOT_TOKEN")  # از env خونده میشه
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_alert(chat_id, text: str):
    """ارسال پیام به تلگرام با async"""
    url = f"{BASE_URL}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})


async def get_follower_count(channel_username: str) -> int:
    """گرفتن تعداد ممبرهای کانال به صورت async"""
    url = f"{BASE_URL}/getChatMemberCount"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={"chat_id": channel_username})
        data = resp.json()
        return data.get("result", 0)


@shared_task
def check_followers():
    """تسک celery برای بررسی فالوئرها"""
    import asyncio
    loop = asyncio.get_event_loop()

    for profile in Profile.objects.all():
        new_count = loop.run_until_complete(get_follower_count(profile.username))

        if profile.follower_count < profile.alert_threshold <= new_count:
            loop.run_until_complete(
                send_alert(profile.telegram_chat_id,
                           f"🎉 {profile.username} به {new_count} عضو رسید!")
            )

        profile.follower_count = new_count
        profile.save()
