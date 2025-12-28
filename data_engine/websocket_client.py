import json
import websocket
import threading
import pandas as pd
from datetime import datetime

class BinanceEngine:
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol 
        print(f"ENGINE INIT: BinanceEngine created for symbol={symbol}")
        self.socket = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
        self.data_buffer = []  # Stores raw trades
        self.history = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'vol'])   
        self.cvd_value = 0.0
        self.cvd_series = []
        self.last_update = datetime.now()
        self.last_price = 0
        self.order_book = {'bids': [], 'asks': []}
        self.cvd_series = []

    def on_message(self, ws, message):
        data = json.loads(message)
        self.last_price = float(data['p'])
        
        # Extract Raw Trade Data
        price = float(data['p'])
        # Only display price if it has changed from previous value
        if price != self.last_price and int(data['E']) % 100 == 0:
            print(f"DEBUG [SOCKET]: Price changed: ${self.last_price} → ${price}")

        quantity = float(data['q'])
        is_buyer_maker = data['m'] # True = Sell Order (Hit Bid), False = Buy Order (Lift Offer)

        # Update Cumulative Volume Delta (CVD)
        trade_delta = -quantity if is_buyer_maker else quantity
        self.cvd_value += trade_delta
        
        # Store for aggregation
        self.data_buffer.append({
            'time': data['E'],
            'price': price,
            'vol': quantity,
            'delta': trade_delta
        })

        # Aggregation Trigger (Every 5 Minutes)
        if len(self.data_buffer) > 0 and (data['E'] // 1000) % 300 == 0:
            print(f"DEBUG [ENGINE]: Triggering aggregation for {len(self.data_buffer)} trades...")
            self._aggregate_candles()

    def _aggregate_candles(self):
        """Transforms raw trades into OHLCV + Indicators"""
        df_raw = pd.DataFrame(self.data_buffer)
        
        # Calculate Candle
        new_row = {
            'close': df_raw['price'].iloc[-1],
            'vol': df_raw['vol'].sum(),
            'cvd': self.cvd_value
        }
        
        self.history = pd.concat([self.history, pd.DataFrame([new_row])]).tail(500)
        self.cvd_series.append(self.cvd_value)
        self.data_buffer = [] # Clear buffer for next candle
        print(f"DEBUG [ENGINE]: 5m candle aggregated. Close: ${new_row['close']}, Vol: {new_row['vol']}")

    '''
    def get_snapshot(self):
        """
        Returns the current market state. 
        Falls back to live price if historical data isn't fully loaded yet.
        """
        # 1. Check if history exists, otherwise use a placeholder
        has_history = hasattr(self, 'history') and not self.history.empty
        close_prices = self.history['close'] if has_history else pd.Series([0])

        # 2. Use the absolute latest price from the live trade stream 
        # (Ensure self.last_price is updated in your 'on_message' function)
        current_price = getattr(self, 'last_price', 0)
        
        # If last_price is missing, try to get it from history
        if current_price == 0 and has_history:
            current_price = close_prices.iloc[-1]

        # 3. Handle Indicators (RSI/EMA require a minimum number of points)
        # If history is too short, we return 'None' or '0' for these specific values
        data_ready = len(close_prices) > 20 

        return {
            "price": current_price,
            "curr_vol": self.history['vol'].iloc[-1] if has_history else 0,
            "avg_vol": self.history['vol'].mean() if has_history else 1,
            "vol_24h": self.history['vol'].tail(288).sum() if has_history else 0,
            "vol_prev_hour": self.history['vol'].tail(12).sum() if has_history else 0,
            "cvd_series": self.cvd_series[-10:] if hasattr(self, 'cvd_series') else [],
            "rsi": self._calculate_rsi(close_prices) if data_ready else 50, # Neutral 50
            "ema_data": {
                "ema20": self._calculate_ema(close_prices, 20) if data_ready else current_price,
                "ema50": self._calculate_ema(close_prices, 50) if data_ready else current_price,
                "ema200": self._calculate_ema(close_prices, 200) if data_ready else current_price
            },
            "bid_vol": self.order_book.get('bids', 0),
            "ask_vol": self.order_book.get('asks', 0),
            "market_cap": 800000000000, 
            "sr_levels": self._get_sr_mock() 
        }
    '''
    def get_snapshot(self):
        # 1. Check if we actually have history data
        has_data = not self.history.empty and 'vol' in self.history.columns
        
        # 2. Calculate volume safely
        if has_data:
            v_24h = self.history['vol'].tail(288).sum()
            v_prev = self.history['vol'].tail(12).sum()
            curr_v = self.history['vol'].iloc[-1]
            avg_v = self.history['vol'].mean()
        else:
            v_24h = 0
            v_prev = 0
            curr_v = 0
            avg_v = 1 # Avoid division by zero later

        # 3. Handle Indicators (RSI/EMA) safely
        # Only calculate if we have enough rows (e.g., 20 for EMA20)
        data_ready = len(self.history) >= 20

        # Prepare Snapshot
        print(f"DEBUG [ENGINE]: Snapshot requested. Price: ${self.last_price}, History Rows: {len(self.history)}")
        return {
            "price": self.last_price,
            "curr_vol": curr_v,
            "avg_vol": avg_v,
            "vol_24h": v_24h,
            "vol_prev_hour": v_prev,
            "rsi": self._calculate_rsi() if data_ready else 50,
            "ema_data": {
                "ema20": self._calculate_ema(20) if data_ready else [self.last_price, self.last_price],
                "ema50": self._calculate_ema(50) if data_ready else [self.last_price, self.last_price],
                "ema200": self._calculate_ema(200) if data_ready else [self.last_price, self.last_price]
            },
            "bid_vol": self.order_book.get('bids', []),
            "ask_vol": self.order_book.get('asks', []),
            "sr_levels": self._get_sr_mock(),
            "nearest_sr_value": max(self.last_price * 0.98, 1),  # Prevent 0
            "best_bid": max(self.last_price * 0.9999, 1),
            "best_ask": max(self.last_price * 1.0001, 1),
            "cvd_series": self.cvd_series[-10:] if len(self.cvd_series) > 0 else [0],
            "market_cap": 800000000000
        }


    def _calculate_rsi(self, period=14):
        """Calculate RSI from history."""
        if len(self.history) < period or 'close' not in self.history.columns:
            return 50
        series = self.history['close']
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        print(f"DEBUG [ENGINE]: RSI({period}) calculated: {rsi:.2f}")
        return rsi
    
    def _get_sr_mock(self):
        """Temporary mock for Support & Resistance levels."""
        # This just gives the system some fake numbers to work with until you build the real logic
        current = getattr(self, 'last_price', 90000)
        # Return format expected by sr_thresholds.py: {"7d": {"sup": val, "res": val}, ...}
        return {
            "7d": {"sup": current * 0.98, "res": current * 1.02, "breached": False},
            "30d": {"sup": current * 0.95, "res": current * 1.05, "breached": False}
        }

    def _calculate_ema(self, window):
        """Calculate EMA from history."""
        if len(self.history) < window or 'close' not in self.history.columns:
            return [self.last_price, self.last_price]
        series = self.history['close']
        ema = list(series.ewm(span=window, adjust=False).mean().tail(2))
        print(f"DEBUG [ENGINE]: EMA({window}) calculated. Latests: {ema}")
        return ema

    def start(self):
        ws = websocket.WebSocketApp(self.socket, on_message=self.on_message)
        ws.run_forever()

# Execution Thread (No Main)
# This would be started by the Web Server at runtime
engine = BinanceEngine()
thread = threading.Thread(target=engine.start, daemon=True)
thread.start()
print("ENGINE THREAD: BinanceEngine.start() thread launched (daemon)")