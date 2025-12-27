# 🖥️ ALGO_TRADER_SYSTEM V1.0
### Real-Time Market Surveillance & Logic Engine

An automated consultant that monitors Bitcoin price action in real-time. The system processes live trades via the Binance WebSocket API, evaluates them through a 9-metric logic layer, and uses a multi-stage questionnaire system to identify and confirm trade leads. Results are streamed to a custom-built, color-coded terminal interface on a local web server.

---

## 🏗️ System Architecture

The system is designed as a modular pipeline:
1.  **Data Engine:** A high-speed WebSocket client that buffers trade data into memory.
2.  **Metric Layer:** 9 standalone modules that calculate technical indicators (RSI, EMA, Volume Spikes, etc.).
3.  **Questionnaire Engine:** A logic gate system (Q1–Q5) that filters market noise into actionable leads.
4.  **Web Interface:** A Flask-SocketIO server that pushes live "micro-decisions" and "final verdicts" to a retro terminal UI.

---

## 📂 Directory Structure

```text
ALGO_TRADER_SYSTEM/
├── data_engine/           # Live WebSocket & Data Snapshotting
│   ├── __init__.py
│   └── websocket_client.py
├── metrics/                # Mathematical Indicators
│   ├── __init__.py
│   ├── rsi_logic.py
│   ├── volume_spike.py
│   └── ... (9 modules)
├── questionnaires/         # Decision-Making Logic
│   ├── __init__.py
│   ├── q1_breakthrough.py
│   ├── q2_interest.py     # Main Entry Gate
│   ├── q3_aggressive.py
│   └── q5_hold_logic.py
├── web_interface/          # Visual Dashboard
│   ├── app.py              # Orchestrator & Web Server
│   └── templates/
│       └── index.html      # Terminal UI Frontend
├── requirements.txt        # Dependencies
├── diagnose.py             # System Health Check
└── test_ui.py              # UI Visual Stress Test

