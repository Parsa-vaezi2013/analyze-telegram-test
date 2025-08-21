import httpx
import asyncio
from celery import shared_task
from django.conf import settings
from .models import Profile

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

async def send_alert(chat_id: int, text: str, client: httpx.AsyncClient):
    await client.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

async def get_follower_count(chat_id_or_username: str, client: httpx.AsyncClient) -> int:
    r = await client.get(f"{BASE_URL}/getChatMemberCount", params={"chat_id": chat_id_or_username})
    if not r.is_success:
        return 0
    data = r.json()
    return int(data.get("result", 0) or 0)

async def _check_followers_async():
    async with httpx.AsyncClient(timeout=10) as client:
        for profile in Profile.objects.all():
            new_count = await get_follower_count(profile.username, client)
            if profile.follower_count < profile.alert_threshold <= new_count:
                await send_alert(
                    settings.TELEGRAM_CHANNEL_ID,
                    f"🎉 {profile.username} به {new_count} عضو رسید!",
                    client,
                )
            profile.follower_count = new_count
            profile.save(update_fields=["follower_count"])

@shared_task
def check_followers():
    asyncio.run(_check_followers_async())
