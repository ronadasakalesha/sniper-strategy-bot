import os
from delta_rest_client import DeltaRestClient
from dotenv import load_dotenv

load_dotenv()

class DeltaClient:
    def __init__(self):
        self.api_key = os.getenv("DELTA_API_KEY")
        self.api_secret = os.getenv("DELTA_API_SECRET")
        self.base_url = os.getenv("DELTA_BASE_URL", "https://api.india.delta.exchange")
        
        self.client = DeltaRestClient(
            base_url=self.base_url,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def get_ohlcv(self, symbol, timeframe, limit=100):
        """
        Fetch historical candle data.
        timeframe: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'
        """
        # Note: Delta API might use different strings for resolutions. 
        # Usually '720' for 12h.
        resolution = '720' if timeframe == '12h' else timeframe
        
        try:
            response = self.client.get_history(
                symbol=symbol,
                resolution=resolution,
                count=limit
            )
            return response
        except Exception as e:
            print(f"Error fetching OHLCV: {e}")
            return []

    def place_order(self, symbol, side, order_type, quantity):
        """
        Place a market or limit order.
        side: 'buy' or 'sell'
        order_type: 'market' or 'limit'
        """
        try:
            # Simple market order for this strategy
            order_data = {
                "product_id": self.get_product_id(symbol),
                "side": side,
                "order_type": order_type,
                "size": quantity
            }
            response = self.client.place_order(order_data)
            return response
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def get_product_id(self, symbol):
        """
        Get product_id for a symbol string (e.g., 'BTCINR').
        """
        # This usually needs a lookup from the API. For simplicity:
        products = self.client.get_products()
        for p in products:
            if p['symbol'] == symbol:
                return p['id']
        raise ValueError(f"Symbol {symbol} not found on Delta Exchange.")

    def get_balance(self, asset='INR'):
        """
        Fetch account balance.
        """
        try:
            balances = self.client.get_balances()
            for b in balances:
                if b['asset_symbol'] == asset:
                    return b['balance']
            return 0
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0
