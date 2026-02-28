import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DeltaClient:
    def __init__(self):
        self.base_url = os.getenv("DELTA_BASE_URL", "https://api.india.delta.exchange")
        
    def get_ohlcv(self, symbol, timeframe, limit=100):
        """
        Fetch historical candle data from public API.
        timeframe: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'
        """
        resolution = '720' if timeframe == '12h' else timeframe
        
        # Public history endpoint: /v2/history/candles
        url = f"{self.base_url}/v2/history/candles"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "count": limit
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            # Delta returns result in 'result' key
            if data.get('success'):
                return data.get('result', [])
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
