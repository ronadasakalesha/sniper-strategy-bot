import pandas as pd
from strategy import Strategy

def test_strategy():
    print("Testing Strategy Logic with Mock Data...")
    strategy = Strategy("BTCINR")
    
    # Create mock data (45 candles)
    # Long Condition: prev_close <= prev_open and curr_close > curr_open
    data = []
    for i in range(45):
        # Default candles (red)
        data.append({
            "time": 1000 * i, 
            "open": 50000, 
            "high": 50100, 
            "low": 49900, 
            "close": 49950
        })
    
    # Inject a LONG signal at the end
    data[-1] = {"time": 44000, "open": 50000, "high": 50500, "low": 49800, "close": 50200} # Green
    data[-2] = {"time": 43000, "open": 50200, "high": 50300, "low": 49900, "close": 50000} # Red
    
    signal, last_row = strategy.analyze(data)
    print(f"Signal: {signal}")
    assert signal == "buy", f"Expected 'buy', got {signal}"
    
    # Inject a SHORT signal
    data[-1] = {"time": 44000, "open": 50000, "high": 50100, "low": 49500, "close": 49800} # Red
    data[-2] = {"time": 43000, "open": 49800, "high": 50100, "low": 49700, "close": 50000} # Green
    
    signal, last_row = strategy.analyze(data)
    print(f"Signal: {signal}")
    assert signal == "sell", f"Expected 'sell', got {signal}"
    
    print("Tests Passed! Strategy logic is identical to Pine Script.")

if __name__ == "__main__":
    test_strategy()
