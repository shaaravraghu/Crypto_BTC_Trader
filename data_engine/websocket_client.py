import json
import websocket
import threading
import pandas as pd
from datetime import datetime

class BinanceEngine:
    def __init__(self, symbol="btcusdt"):
        self.socket = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
        self.data_buffer = []  # Stores raw trades
        self.history = pd.DataFrame()  # Stores aggregated 5m candles
        self.order_book = {"bids": 0.0, "asks": 0.0}
        self.cvd_value = 0.0
        self.cvd_series = []
        self.last_update = datetime.now()

    def on_message(self, ws, message):
        data = json.loads(message)
        
        # Extract Raw Trade Data
        price = float(data['p'])
        if int(data['E']) % 100 == 0:
            print(f"DEBUG [SOCKET]: Receiving live trades. Current BTC Price: ${price}")

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

    def get_snapshot(self):
        """
        The Standardized Data Form consumed by all Questionnaires.
        """
        # Calculate Technicals on the fly for the snapshot
        close_prices = self.history['close'] if not self.history.empty else pd.Series([0])
        
        return {
            "price": close_prices.iloc[-1] if not close_prices.empty else 0,
            "curr_vol": self.history['vol'].iloc[-1] if not self.history.empty else 0,
            "avg_vol": self.history['vol'].mean() if not self.history.empty else 1,
            "vol_24h": self.history['vol'].tail(288).sum(), # 288 * 5m = 24h
            "vol_prev_hour": self.history['vol'].tail(12).sum(),
            "cvd_series": self.cvd_series[-10:],
            "rsi": self._calculate_rsi(close_prices),
            "ema_data": {
                "ema20": self._calculate_ema(close_prices, 20),
                "ema50": self._calculate_ema(close_prices, 50),
                "ema200": self._calculate_ema(close_prices, 200)
            },
            "bid_vol": self.order_book['bids'],
            "ask_vol": self.order_book['asks'],
            "market_cap": 800000000000, # Placeholder or API fetch
            "sr_levels": self._get_sr_mock() # Logic for S/R detection
        }

    def _calculate_rsi(self, series, period=14):
        if len(series) < period: return 50
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]

    def _calculate_ema(self, series, window):
        return list(series.ewm(span=window, adjust=False).mean().tail(2))

    def start(self):
        ws = websocket.WebSocketApp(self.socket, on_message=self.on_message)
        ws.run_forever()

# Execution Thread (No Main)
# This would be started by the Web Server at runtime
engine = BinanceEngine()
thread = threading.Thread(target=engine.start, daemon=True)
thread.start()