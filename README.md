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
│   ├── websocket_client.py
│   └── __init__.py
├── metrics/                # Mathematical Indicators
│   ├── bid_ask_spread.py
│   ├── cvd_analysis.py
│   ├── ema_slope.py
│   ├── order_book_whale.py
│   ├── rsi_logic.py
│   ├── sr_thresholds.py
│   ├── turnover_ratio.py
│   ├── vol_24h.py
│   ├── vol_spike.py
│   └── __init__.py
├── questionnaires/        # Decision-Making Logic (Q1-Q5)
│   ├── q1_breakthrough.py
│   ├── q2_interest.py      # Main Entry Gate
│   ├── q3_aggressive.py
│   ├── q4_efficiency.py
│   ├── q5_hold_logic.py
│   └── __init__.py
├── tests/                 # Unit & Integration Tests
│   ├── test_fictional_data.py
│   ├── test_orchestrator.py
│   ├── test_pipeline.py
│   ├── test_q1_trigger.py
│   ├── test_ui.py
│   └── test_whale_detector.py
├── web_interface/         # Visual Dashboard
│   ├── app.py              # Flask-SocketIO Entry Point
│   └── templates/
│       ├── index.html      # Dashboard Console
│       ├── metric.html     # Metric Detail View
│       └── questionnaire.html # Decision Detail View
├── orchestrator.py        # System logic coordinator
├── whale_detector.py      # Real-time whale tracking monitor
├── requirements.txt       # Dependencies
├── diagnose.py            # System Health Check
└── README.md
```


# Crypto Market Research Overview


## Market Regime Check
The global crypto market cap stands at **$3B**, indicating a **highly volatile** environment. Market structure remains concentrated, with **Bitcoin commanding ~60% dominance**, reinforcing its role as the primary liquidity and sentiment driver. Price discovery across altcoins is largely derivative of BTC’s direction.


**Top 10 Assets by Market Cap:** 
BTC, ETH, USDT, BNB, XRP, USDC, SOL, TRX, DOGE, ADA


---


## Liquidity & Volume Health
- **24H Trading Volume:** Measures real-time market participation and capital flow.
- **Volume Spike Ratio:** Elevated ratios signal sudden interest, speculative activity, or potential manipulation.
- **Cumulative Volume Delta (CVD):** Indicates aggressiveness of buyers vs sellers.
- **Large Order Book Activity:** Highlights whale presence and institutional positioning.
- **Turnover Ratio (Volume / Market Cap):** Higher ratios reflect efficient capital rotation.
- **Bid–Ask Spread:** Tight spreads imply deep liquidity; wider spreads suggest execution risk and lower immediacy.


---


## Market Capitalization Tiers
- **Large Cap ($10B+):** Lower volatility, higher liquidity, reduced downside risk. (PROGRAMMED SPECIALLY FOR BIG CAP CRYPTO'S)
- **Mid Cap:** Balanced risk-return profile with growth potential.
- **Small Cap:** High volatility, asymmetric upside, elevated drawdown risk.


---


## Trend Direction
- **20 EMA (Short Term):** Captures immediate momentum and tactical trend shifts.
- **50 EMA (Medium Term):** Defines swing structure and trend continuation.
- **200 EMA (Long Term):** Core trend filter; above = bullish regime, below = bearish regime.


---


## Momentum Indicators
- **RSI > 70:** Overbought, pullback risk elevated 
- **RSI 50–70:** Bullish momentum 
- **RSI ~50:** Neutral / range-bound 
- **RSI 30–50:** Bearish momentum 
- **RSI < 30:** Oversold, bounce potential


---


## Support & Resistance Zones
- **Short Term:** 7–14 days (tactical entries/exits)
- **Medium Term:** 30–90 days (trend validation)
- **Long Term:** 180–365 days (macro structure and cycle levels)


---


## Tokenomics & Supply Pressure
Assessment of circulating vs total supply, emissions, unlock schedules, burn mechanisms, and staking dynamics. High unlocks increase sell pressure; constrained supply supports price stability.
AVOIDED: QUALITATIVE ANALYSIS


---


## Narrative & Sentiment
Market pricing is heavily influenced by narratives (L1s, AI, RWAs, memes). Sentiment extremes often precede reversals; alignment between narrative strength and on-chain activity is critical.
AVOIDED: QUALITATIVE ANALYSIS


---


## Risk–Reward & Exit Logic
Positions should be evaluated on **asymmetric payoff**: defined downside, scalable upside. Exits are driven by invalidation of trend, momentum divergence, loss of key support, or narrative decay.
AVOIDED: QUALITATIVE ANALYSIS


## METHOD OF APPROACH: Trading Questions -> Micro-Solutions (parameterised) -> Final Verdict


## Questions:
Is there a breakthrough in support/ resistance? Remain Cautious
Sudden interest? A sudden interest in X
Aggressive trading? Yes
Current trading efficiency? High
How long to hold? Short, Long, Medium


## Micro-Solutions (parameterised):


**2. Sudden interest?**


Keeps looking for market variations until trading interest every 10 standard minutes. Notify the trader for activity. Notify for collective points >= 6.


   (+2 points) 24 Hour Trading Volume: total value traded in last 24 hours
   - check for 50% increase in volume as compared to previous hour
   (+3 points) Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation
   - check for values >1.5
   (+2 points) Large Order Book (bid/ ask): whale activity
   - check for value < 0.67 for whale short activity and value > 1.5 for whale buying activity
   (+2 points) Support/ Resistance Thresholds Variables: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)
   - check if the market price < 1% threshold value
   (+1 points) Bid-Ask Spread: shows cost variation; tight spread (high liquidity), wide spread (low liquidity); sign of immediacy
   - value < 0.3% is favourable  


**3. Aggressive trading?**


After there is a positive change in interest, market direction should be ascertained and buy/ sell/ wait verdict should be taken. After the verdict, current trading efficiency should be checked for a decision to roll out. Verdict >= 7. Keep trying every 5 minutes (max 3 times).


   (+2.5 points) Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation
   - check for values >1.5
   (+3.33 points) Cumulative Volume Delta: market aggressiveness
   - CVD slope should be positive (buying/ squaring) and negative (shorting/ selling) for last 4 candles of 5 minutes each
   (+2.5 points) Large Order Book (bid/ ask): whale activity
   - check for value < 0.67 for whale short activity and value > 1.5 for whale buying activity
   (+2 points) Broken Support/ Resistance Thresholds: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)
   - break acceptance threshold value >= 0.5%
   (+1.5 points) Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term)
   - positive slope (bullish bias) & negative slope (bearish bias)


**1. Is there a breakthrough in support/ resistance?**


After there is a positive change in interest, market direction should be ascertained and buy/ sell/ wait verdict should be taken after crossing 5% of threshold value. Verdict >= 5. Keep trying every 5 minutes (max 3 times).


   (+3 points) Broken Support/ Resistance Thresholds: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)
   - threshold should be breached at least once in the past
   (+1.5 points) Relative Strength Index: >70 (Overbought), 50-70 (Bullish), ~50 (Neutral), 30-50 (Bearish), <30 (Oversold)
   - RSI between 52-67 for buying and 33-48 for selling
   (+1.5 points) Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term)
   - positive slope preferred for buying and negative for selling
   - 200 EMA > 50 EMA > 20 EMA (preferance)
   (+2 points) Large Order Book (bid/ ask): whale activity
   - check for value < 0.67 for whale short activity and value > 1.5 for whale buying activity


**2. Current trading efficiency?**


Return decision to aggressive trading. Verdict >= 2.


   (+2 points) Turnover Ratio (Volume/ Market Cap): trading efficiency
   (+1.5 points) Bid-Ask Spread: shows cost variation; tight spread (high liquidity), wide spread (low liquidity); sign of immediacy
   - value < 0.3% is favourable
   (+0.5 points) Relative Strength Index: >70 (Overbought), 50-70 (Bullish), ~50 (Neutral), 30-50 (Bearish), <30 (Oversold)
   - RSI between 52-67 for buying and 33-48 for selling


**5. How long to hold?**


To be checked after every buy/ sell decision. Print out the decisions/ suggestions here. No points.


   Short (Intra-day):
   Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation
   Cumulative Volume Delta: market aggressiveness


   Medium ()/ Long ():
   Relative Strength Index: >70 (Overbought), 50-70 (Bullish), ~50 (Neutral), 30-50 (Bearish), <30 (Oversold)
   Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term)


## Final Verdict: Points based evaluation


---
