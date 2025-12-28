import time
from datetime import datetime

class WhaleDetector:
    """
    Monitors for whale orders (large trades > $500,000 USD value).
    Runs every 10 minutes and displays detected whales.
    """
    def __init__(self, engine, ui_callback=None):
        self.engine = engine
        self.ui_callback = ui_callback
        self.whale_threshold = 500000  # $500k USD
        self.detected_whales = []
        self.running = False
    
    def log(self, msg, color="#ffffff"):
        """Log to terminal and UI."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [WHALE DETECTOR] {msg}")
        if self.ui_callback:
            self.ui_callback(f"🐋 {msg}", color)
    
    def detect_whales(self):
        """
        Analyzes recent order book data for whale activity.
        A whale is defined as any single order with value > $500k.
        """
        print("[WHALE DETECTOR] Scanning for whale orders...")
        
        current_price = self.engine.last_price
        if current_price == 0:
            print("[WHALE DETECTOR] No price data available yet.")
            return []
        
        whales_found = []
        
        # Check bid side (buy orders)
        bids = self.engine.order_book.get('bids', [])
        for bid in bids:
            if isinstance(bid, list) and len(bid) >= 2:
                price = float(bid[0])
                quantity = float(bid[1])
                value_usd = price * quantity
                
                if value_usd > self.whale_threshold:
                    whale_info = {
                        'type': 'BUY',
                        'price': price,
                        'quantity': quantity,
                        'value_usd': value_usd,
                        'timestamp': datetime.now()
                    }
                    whales_found.append(whale_info)
        
        # Check ask side (sell orders)
        asks = self.engine.order_book.get('asks', [])
        for ask in asks:
            if isinstance(ask, list) and len(ask) >= 2:
                price = float(ask[0])
                quantity = float(ask[1])
                value_usd = price * quantity
                
                if value_usd > self.whale_threshold:
                    whale_info = {
                        'type': 'SELL',
                        'price': price,
                        'quantity': quantity,
                        'value_usd': value_usd,
                        'timestamp': datetime.now()
                    }
                    whales_found.append(whale_info)
        
        return whales_found
    
    def display_whales(self, whales):
        """Display detected whales in a formatted manner."""
        if not whales:
            print("[WHALE DETECTOR] No whale orders detected (>$500k).")
            return
        
        print(f"\n{'='*70}")
        print(f"🐋 WHALE ALERT: {len(whales)} Large Order(s) Detected!")
        print(f"{'='*70}")
        
        for i, whale in enumerate(whales, 1):
            whale_type = whale['type']
            color = "#2ecc71" if whale_type == "BUY" else "#e74c3c"
            
            msg = (f"Whale #{i} | {whale_type} | "
                   f"${whale['value_usd']:,.2f} USD | "
                   f"Price: ${whale['price']:,.2f} | "
                   f"Qty: {whale['quantity']:.4f} BTC")
            
            print(f"  {msg}")
            self.log(msg, color)
        
        print(f"{'='*70}\n")
    
    def run_monitor(self):
        """Main monitoring loop - runs every 10 minutes."""
        print("[WHALE DETECTOR] Starting whale monitoring (10 min interval)...")
        self.running = True
        
        while self.running:
            try:
                # Wait for engine to be ready
                if self.engine.last_price == 0:
                    time.sleep(10)
                    continue
                
                # Detect whales
                whales = self.detect_whales()
                
                # Add to history and display
                if whales:
                    self.detected_whales.extend(whales)
                    self.display_whales(whales)
                else:
                    print(f"[WHALE DETECTOR] Scan complete. No whales detected at {datetime.now().strftime('%H:%M:%S')}")
                
                # Sleep for 10 minutes
                time.sleep(600)
                
            except Exception as e:
                print(f"[WHALE DETECTOR] Error: {e}")
                time.sleep(60)
    
    def get_recent_whales(self, minutes=60):
        """Get whales detected in the last N minutes."""
        cutoff_time = datetime.now().timestamp() - (minutes * 60)
        recent = [w for w in self.detected_whales 
                  if w['timestamp'].timestamp() > cutoff_time]
        return recent
    
    def stop(self):
        """Stop the monitoring loop."""
        self.running = False
        print("[WHALE DETECTOR] Stopping...")
