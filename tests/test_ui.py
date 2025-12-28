import socketio
import time

# This script pretends to be the backend to test your UI colors
sio = socketio.Client()

try:
    sio.connect('http://127.0.0.1:5001') # Use the port you set (5001 or 5000)
    print("Connected to Terminal UI. Injecting Test Data...")

    logs = [
        {"msg": "TEST: Initializing Logic Engine...", "color": "#ffffff"},
        {"msg": "Q2: Market survey initiated.", "color": "#3498db"},
        {"msg": "  [Micro] RSI: PASS (Target < 30)", "color": "#00ffff"},
        {"msg": "  [Micro] VOL: PASS (Spike Detected)", "color": "#00ffff"},
        {"msg": "SUCCESS: Lead Generated (Total Points: 7.5)", "color": "#2ecc71"},
        {"msg": "Q5 VERDICT: Aggressive Intra-day scalp recommended.", "color": "#9b59b6"}
    ]

    for log in logs:
        sio.emit('new_log', {'time': 'TEST', 'msg': log['msg'], 'color': log['color']})
        time.sleep(1)

    print("Injection complete. Check your browser!")
    sio.disconnect()
except Exception as e:
    print(f"Error: {e}. Make sure app.py is running first!")

    