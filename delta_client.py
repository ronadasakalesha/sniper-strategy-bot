import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class DeltaClient:
    def __init__(self):
        self.base_url = os.getenv("DELTA_BASE_URL", "https://api.india.delta.exchange")
        
    def get_ohlcv(self, symbol, timeframe, limit=100):
        """
        Fetch historical candle data from public API.
        Valid timeframes: '1m','3m','5m','15m','30m','1h','2h','4h','6h','12h','1d','1w'
        """
        # Resolution in minutes for calculating start timestamp
        resolution_minutes = {
            '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '2h': 120, '4h': 240, '6h': 360,
            '12h': 720, '1d': 1440, '1w': 10080
        }.get(timeframe, 720)
        
        # Calculate start/end timestamps (seconds)
        end_ts = int(time.time())
        start_ts = end_ts - (resolution_minutes * 60 * limit)
        
        url = f"{self.base_url}/v2/history/candles"
        params = {
            "symbol": symbol,
            "resolution": timeframe,  # Must be string like '12h', NOT integer
            "start": start_ts,
            "end": end_ts
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                return data.get('result', [])
            print(f"API error: {data}")
            return []
        except Exception as e:
            print(f"Error fetching OHLCV: {e}")
            return []

    def get_product_id(self, symbol):
        """
        Get product_id for a symbol string (Public).
        """
        url = f"{self.base_url}/v2/products"
        try:
            response = requests.get(url)
            response.raise_for_status()
            products = response.json().get('result', [])
            for p in products:
                if p['symbol'] == symbol:
                    return p['id']
            raise ValueError(f"Symbol {symbol} not found.")
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None

    def get_product_id(self, symbol):
        """
        Get product_id for a symbol string (Public).
        """
        url = f"{self.base_url}/v2/products"
        try:
            response = requests.get(url)
            response.raise_for_status()
            products = response.json().get('result', [])
            for p in products:
                if p['symbol'] == symbol:
                    return p['id']
            raise ValueError(f"Symbol {symbol} not found.")
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None
