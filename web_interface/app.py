import threading
import time
import traceback
import sys
import os
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from questionnaires import q2_interest, q1_breakthrough, q3_aggressive


# 1. Path Setup: Ensure custom modules are discoverable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 2. Module Imports
try:
    from data_engine.websocket_client import BinanceEngine
    print("WEB_APP: Custom modules loaded successfully.")
except ImportError as e:
    print(f"WEB_APP CRITICAL: Failed to import modules. {e}")
    sys.exit(1)

# 3. Flask & SocketIO Setup
app = Flask(__name__)
# cors_allowed_origins="*" is important for local development
socketio = SocketIO(app, cors_allowed_origins="*")

# 4. Global Logging Helper
def ui_log(msg, color="#ffffff"):
    """Pushes logs to the Web UI and prints them to the local terminal."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Print to terminal so we can see it even if the browser is closed
    print(f"[{timestamp}] [UI_LOG]: {msg}")
    socketio.emit('new_log', {
        'time': timestamp, 
        'msg': msg, 
        'color': color
    })
    print(f"DEBUG [SERVER]: Log emitted to UI via SocketIO - {msg[:50]}...")

# 5. The Background Brain (Orchestrator)
# Initialize Orchestrator globally
from orchestrator import SystemOrchestrator
orchestrator = None

# 6. Web Routes
@app.route('/')
def index():
    print("DEBUG [SERVER]: Route accessed: / (Dashboard)")
    return render_template('index.html')

@app.route('/questionnaires/q1')
def page_q1():
    print("DEBUG [SERVER]: Route accessed: /questionnaires/q1")
    return render_template('questionnaire.html', title="Q1: Breakthrough", endpoint="q1")

@app.route('/questionnaires/q2')
def page_q2():
    print("DEBUG [SERVER]: Route accessed: /questionnaires/q2")
    return render_template('questionnaire.html', title="Q2: Interest Survey", endpoint="q2")

@app.route('/questionnaires/q3')
def page_q3():
    print("DEBUG [SERVER]: Route accessed: /questionnaires/q3")
    return render_template('questionnaire.html', title="Q3: Aggression", endpoint="q3")

@app.route('/questionnaires/q4')
def page_q4():
    print("DEBUG [SERVER]: Route accessed: /questionnaires/q4")
    return render_template('questionnaire.html', title="Q4: Efficiency", endpoint="q4")

@app.route('/questionnaires/q5')
def page_q5():
    print("DEBUG [SERVER]: Route accessed: /questionnaires/q5")
    return render_template('questionnaire.html', title="Q5: Consultation", endpoint="q5")

@app.route('/metrics/<name>')
def page_metric(name):
    print(f"DEBUG [SERVER]: Route accessed: /metrics/{name}")
    return render_template('metric.html', metric_name=name)

# 7. Execution Entry Point
if __name__ == '__main__':
    print(f"WEB_APP: Launching server on http://127.0.0.1:5001")
    
    # Initialize Orchestrator with UI Callback
    orchestrator = SystemOrchestrator(ui_callback=ui_log)
    orchestrator.start()
    
    # Run Flask-SocketIO
    socketio.run(app, port=5001, debug=False)