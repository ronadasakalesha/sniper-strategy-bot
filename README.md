# Delta India SniperX Bot

This bot automates the SniperX V3 strategy on Delta Exchange India (api.india.delta.exchange). It uses a 12-hour timeframe and executes trades based on candle crossover/crossunder logic.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Credentials**:
   - Copy `.env.example` to `.env`.
   - Fill in your `DELTA_API_KEY` and `DELTA_API_SECRET` from your Delta India account.

3. **Verify Logic (Dry Run)**:
   - Run the dry run script to see historical signals without placing orders.
   ```bash
   python dry_run.py
   ```

4. **Run the Bot**:
   - Start the main bot for live trading.
   ```bash
   python main.py
   ```

## Strategy Logic
- **Timeframe**: 12 Hours.
- **Buy Signal**: A green candle that follows a red/doji candle.
- **Sell Signal**: A red candle that follows a green/doji candle.
