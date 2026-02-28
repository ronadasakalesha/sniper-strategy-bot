import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from delta_client import DeltaClient
from strategy import Strategy

load_dotenv()

def datetime_from_utc_to_local(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

def dry_run():
    symbol = os.getenv("SYMBOL", "BTCINR")
    print(f"--- Dry Run for {symbol} ---")
    
    client = DeltaClient()
    strategy = Strategy(symbol)
    
    # Fetch 100 historical candles (12h)
    data = client.get_ohlcv(symbol, "12h", limit=100)
    
    if not data:
        print("No data received. Ensure DELTA_API_KEY and SECRET are set in .env (if needed for history).")
        return

    df = pd.DataFrame(data)
    print(f"Analyzing {len(df)} historical candles...")
    
    for i in range(40, len(df)):
        subset = data[:i+1]
        signal, last_row = strategy.analyze(subset)
        
        if signal != 'hold':
            timestamp = datetime_from_utc_to_local(last_row['time'])
            print(f"[{timestamp}] Signal: {signal.upper()} at Price: {last_row['close']}")

if __name__ == "__main__":
    dry_run()
