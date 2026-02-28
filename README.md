# Delta India SniperX Telegram Bot

This bot monitors the SniperX V3 strategy on Delta Exchange India and sends alerts to your Telegram channel. It uses the 12-hour timeframe and public market data (no API keys required).

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Telegram Bot Setup**:
    - Message [@BotFather](https://t.me/botfather) on Telegram to create a bot and get your **API Token**.
    - Message [@userinfobot](https://t.me/userinfobot) to get your **Chat ID**.
    - Open your bot in Telegram and click **Start**.

3.  **Configure Environment**:
    - Copy `.env.example` to `.env`.
    - Fill in your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

4.  **Run Locally**:
    ```bash
    python main.py
    ```

5.  **Deploy to Railway**:
    - Push your code to GitHub.
    - Connect your repo to [Railway.app](https://railway.app/).
    - Add your `.env` variables in the Railway "Variables" tab.

## Strategy Logic
- **Timeframe**: 12 Hours.
- **Buy Alert**: Green candle crossover.
- **Sell Alert**: Red candle crossunder.
