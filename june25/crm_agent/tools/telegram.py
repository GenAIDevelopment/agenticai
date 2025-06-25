import os
import asyncio
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests

load_dotenv()


#@tool("telegram_sender", parse_docstring=True, return_direct=True)
# async def send_group_notification(message:str):
#     """Sends telegram notifications to the group

#     Args:
#         message (str): message
#     """
#     bot = Bot(token=os.getenv('TELEGRAM_BOT_APIKEY'))
#     async with bot:
#         bot.send_message(chat_id=os.getenv('GROUP_CHANNEL_ID'),text= message)

def send_telegram_message( message):
    """
    Sends a message to a Telegram chat via a Telegram bot.

    Args:
        message (str): The text message to send.

    Returns:
        dict: The JSON response from the Telegram API, or None if an error occurred.
    """
    bot_token=os.getenv('TELEGRAM_BOT_APIKEY')
    chat_id=os.getenv('GROUP_CHANNEL_ID')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    

if __name__ == '__main__':
    send_telegram_message(message="Hello")
