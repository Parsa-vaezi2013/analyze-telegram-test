from telegram import Bot

BOT_TOKEN = '8171301737:AAGUb8GQ6M8TqIvOFARMpCJjVIz7hnhry00'
bot = Bot(token=BOT_TOKEN)

def send_alert(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message )


