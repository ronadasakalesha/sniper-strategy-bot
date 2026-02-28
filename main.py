import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from delta_client import DeltaClient
from strategy import Strategy

load_dotenv()

# Configuration
SYMBOL = os.getenv("SYMBOL", "BTCINR")
QUANTITY = float(os.getenv("QUANTITY", "0.001"))
CHECK_INTERVAL = 60  # seconds

STATE_FILE = "bot_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_signal": None, "last_timestamp": None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def main():
    print(f"Starting Delta India SniperX Bot for {SYMBOL}...")
    client = DeltaClient()
    strategy = Strategy(SYMBOL)
    state = load_state()

    while True:
        try:
            # 1. Fetch data (12h timeframe)
            data = client.get_ohlcv(SYMBOL, "12h")
            if not data:
                print("Failed to fetch data. Retrying...")
                time.sleep(CHECK_INTERVAL)
                continue

            # 2. Analyze
            signal, last_row = strategy.analyze(data)
            current_timestamp = last_row.get('time')

            # 3. Decision Logic
            if signal != 'hold' and current_timestamp != state.get("last_timestamp"):
                print(f"[{datetime.now()}] New Signal: {signal.upper()} at {last_row['close']}")
                
                # Execute Trade
                side = "buy" if signal == "buy" else "sell"
                response = client.place_order(SYMBOL, side, "market", QUANTITY)
                
                if response:
                    print(f"Order successful: {response}")
                    state["last_signal"] = signal
                    state["last_timestamp"] = current_timestamp
                    save_state(state)
                else:
                    print("Order failed.")
            else:
                # print(f"[{datetime.now()}] No new signal. Last: {state.get('last_signal')}")
                pass

        except Exception as e:
            print(f"Main loop error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
