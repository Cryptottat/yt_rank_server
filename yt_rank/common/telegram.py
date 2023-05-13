import requests
from .models import TelegramInfo


def send_to_telegram(message):
    telegram_info = TelegramInfo.object.all().first()
    if telegram_info is not None:
        apiToken = telegram_info.bot_token
        chatID = telegram_info.chat_id
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            print(response.text)
        except Exception as e:
            print(e)
