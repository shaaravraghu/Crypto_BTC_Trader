import sys
import os

print("--- SYSTEM DIAGNOSTIC ---")
# 1. Check Directory
print(f"Current Directory: {os.getcwd()}")

# 2. Check Imports
try:
    from data_engine.websocket_client import BinanceEngine
    from questionnaires import q2_interest
    from metrics import rsi_logic
    print("✅ All modules imported successfully.")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Check if you have __init__.py in every folder.")

# 3. Check Flask Dependencies
try:
    import flask
    import flask_socketio
    import websocket
    print("✅ Dependencies (Flask, SocketIO, WebSocket) are installed.")
except ImportError as e:
    print(f"❌ Missing Library: {e}. Run 'pip install -r requirements.txt'")
    