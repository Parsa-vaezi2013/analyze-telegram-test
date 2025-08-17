# from telegram import Bot

# BOT_TOKEN = '8171301737:AAGUb8GQ6M8TqIvOFARMpCJjVIz7hnhry00'
# bot = -1002835752715

import requests

BOT_TOKEN = "8171301737:AAGUb8GQ6M8TqIvOFARMpCJjVIz7hnhry00"
CHANNEL_ID = -1002835752715  # آیدی کانال با منفی و 100

def send_alert(chat_id, text):
    """ارسال پیام به چت یا کانال"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=payload)



from telegram import Update
from telegram.ext import ApplicationBuilder, ChatMemberHandler, ContextTypes

BOT_TOKEN = "8171301737:AAGUb8GQ6M8TqIvOFARMpCJjVIz7hnhry00"
CHANNEL_ID = -1002835752715 

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    if old_status in ["left", "kicked"] and new_status == "member":
        user = chat_member.new_chat_member.user
        welcome_text = f"🎉 خوش اومدی {user.first_name}!"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=welcome_text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))

    app.run_polling()
