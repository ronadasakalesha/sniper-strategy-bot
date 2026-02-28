import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, message):
        if not self.token or not self.chat_id:
            print("Telegram credentials missing.")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Telegram error: {e}")
            return False

    def send_signal(self, symbol, signal, price):
        emoji = "🚀" if signal == "buy" else "📉"
        action = "BULLISH" if signal == "buy" else "BEARISH"
        
        msg = (
            f"*SniperX V3 Signal Alert* {emoji}\n\n"
            f"Symbol: `{symbol}`\n"
            f"Direction: *{action}*\n"
            f"Timeframe: `12 Hours`\n"
            f"Price: `{price}`\n\n"
            f"⚠️ _Manual entry suggested based on your confirmation._"
        )
        return self.send_message(msg)
