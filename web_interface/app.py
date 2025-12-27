import threading
import time
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
import os

# Add the parent directory (ALGO_TRADER_SYSTEM) to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your custom modules
from data_engine.websocket_client import BinanceEngine
from questionnaires import q2_interest, q1_breakthrough, q3_aggressive

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Helper to push logs to the UI
def ui_log(msg, color="#ffffff"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    socketio.emit('new_log', {
        'time': timestamp, 
        'msg': msg, 
        'color': color
    })

def system_orchestrator():
    """Runs the background logic without a Main file."""
    print("DEBUG [SYSTEM]: Orchestrator Thread Started.")
    engine = BinanceEngine()
    # Start Binance Socket in its own thread
    threading.Thread(target=engine.start, daemon=True).start()
    print("DEBUG [SYSTEM]: Binance WebSocket thread launched.")

    ui_log("SYSTEM START: Terminal linked to Binance wss://", "#00FF00")
    
    while True:
        print(f"DEBUG [SYSTEM]: Loop Heartbeat at {datetime.now().strftime('%H:%M:%S')}")
        # --- TEST LINE START ---
        ui_log("CONNECTION ALIVE: Waiting for Binance data...", "#888888") 
        # --- TEST LINE END ---
        ui_log("SCANNING MARKET: Fetching latest snapshot...", "#3498db") # Blue

        ui_log("Q2: Initiating 10-minute market survey...", "#3498db") # Blue
        snapshot = engine.get_snapshot()

        if snapshot['price'] == 0:
            print("DEBUG [SYSTEM]: Waiting for data buffer to fill...")
            ui_log("BUFFERING: Collecting initial market data...", "#888888")
        else:
            print(f"DEBUG [SYSTEM]: Snapshot captured. Price: {snapshot['price']}")
            report = q2_interest.survey_market(snapshot)
        # Run Q2 Survey
        report = q2_interest.survey_market(snapshot)
        
        # Log Q2 Micro-decisions
        for metric, data in report['metrics_detail'].items():
            color = "#00ffff" if data['status'] else "#7f8c8d"
            status_text = "PASSED" if data['status'] else "FAILED"
            ui_log(f"  [Micro] {metric}: {status_text} | Points: {data['points']}", color)

        if report['trigger_next']:
            ui_log(f"LEAD GENERATED: Q2 Total Points {report['total_points']}", "#2ecc71") # Green
            
            # Start Q1 and Q3 in parallel threads
            threading.Thread(target=q1_breakthrough.process_lead, args=(engine, ui_log)).start()
            threading.Thread(target=q3_aggressive.process_lead, args=(engine, ui_log)).start()
        else:
            ui_log(f"Q2: Minimum points not reached ({report['total_points']}/6). Standing by.", "#e67e22")

        time.sleep(10) # 10 Minute Cycle

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start the system orchestrator thread
    threading.Thread(target=system_orchestrator, daemon=True).start()
    socketio.run(app, port=5001)

