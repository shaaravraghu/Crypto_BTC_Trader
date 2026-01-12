Market Regime Check:

* Global Crypto Market Cap is $3T  
* Highly volatile  
* BTC alone has 60% market share  
* Top 10 Crypto’s: BTC, ETH, USDT, BNB, XRP, USDC, SOL, TRX, DOGE, ADA

Liquidity & Volume Health:

* 24 Hour Trading Volume: total value traded in last 24 hours  
* Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation  
* Cumulative Volume Delta: market aggressiveness   
* Large Order Book: whale activity  
* Turnover Ratio (Volume/ Market Cap): trading efficiency  
* Bid-Ask Spread: shows cost variation; tight spread (high liquidity), wide spread (low liquidity); sign of immediacy

Market Capitalisation Tier:

* $10B+ (large cap \+ low risk)  
* Mid cap \+ medium risk  
* Small cap \+ high risk

Trend Direction:

* Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term) 

Momentum Indicators:

* Relative Strength Index: \>70 (Overbought), 50-70 (Bullish), \~50 (Neutral), 30-50 (Bearish), \<30 (Oversold)

Support & Resistance Zones:

* Support/ Resistance Thresholds: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)

Tokenomics and Supply Pressure  
Narrative and Sentiment  
Risk-Reward & Exit Logic 

Questions to ask?

1. Is there a breakthrough in support/ resistance? Remain Cautious  
2. Sudden interest? A sudden interest in X  
3. Aggressive trading? Yes  
4. Current trading efficiency? High  
5. How long to hold? Short, Long, Medium

Solutions:

2\. Sudden interest?   
Keeps looking for market variations until trading interest every 10 standard minutes. Notify the trader for activity. Notify for collective points \>= 6\.

* (+2 points) 24 Hour Trading Volume: total value traded in last 24 hours  
  \- check for 50% increase in volume as compared to previous hour  
* (+3 points) Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation  
  \- check for values \>1.5  
* (+2 points) Large Order Book (bid/ ask): whale activity  
  \- check for value \< 0.67 for whale short activity and value \> 1.5 for whale buying activity  
* (+2 points) Support/ Resistance Thresholds Variables: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)  
  \- check if the market price \< 1% threshold value  
* (+1 points) Bid-Ask Spread: shows cost variation; tight spread (high liquidity), wide spread (low liquidity); sign of immediacy   
  \- value \< 0.3% is favourable   

3\. Aggressive trading?   
After there is a positive change in interest, market direction should be ascertained and buy/ sell/ wait verdict should be taken. After the verdict, current trading efficiency should be checked for a decision to roll out. Verdict \>= 7\. Keep trying every 5 minutes (max 3 times).

* (+2.5 points) Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation  
  \- check for values \>1.5  
* (+3.33 points) Cumulative Volume Delta: market aggressiveness   
  \- CVD slope should be positive (buying/ squaring) and negative (shorting/ selling) for last 4 candles of 5 minutes each  
* (+2.5 points) Large Order Book (bid/ ask): whale activity  
  \- check for value \< 0.67 for whale short activity and value \> 1.5 for whale buying activity  
* (+2 points) Broken Support/ Resistance Thresholds: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)  
  \- break acceptance threshold value \>= 0.5%  
* (+1.5 points) Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term)   
  \- positive slope (bullish bias) & negative slope (bearish bias)

1\. Is there a breakthrough in support/ resistance?   
After there is a positive change in interest, market direction should be ascertained and buy/ sell/ wait verdict should be taken after crossing 5% of threshold value. Verdict \>= 5\. Keep trying every 5 minutes (max 3 times).

* (+3 points) Broken Support/ Resistance Thresholds: 7/14 days (short term), 30/90 days (medium term), 180/365 days (long term)  
  \- threshold should be breached at least once in the past  
* (+1.5 points) Relative Strength Index: \>70 (Overbought), 50-70 (Bullish), \~50 (Neutral), 30-50 (Bearish), \<30 (Oversold)  
  \- RSI between 52-67 for buying and 33-48 for selling  
* (+1.5 points) Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term)   
  \- positive slope preferred for buying and negative for selling  
  \- 200 EMA \> 50 EMA \> 20 EMA (preferance)  
* (+2 points) Large Order Book (bid/ ask): whale activity  
  \- check for value \< 0.67 for whale short activity and value \> 1.5 for whale buying activity

4\. Current trading efficiency?  
Return decision to aggressive trading. Verdict \>= 2\.

* (+2 points) Turnover Ratio (Volume/ Market Cap): trading efficiency  
* (+1.5 points) Bid-Ask Spread: shows cost variation; tight spread (high liquidity), wide spread (low liquidity); sign of immediacy   
  \- value \< 0.3% is favourable   
* (+0.5 points) Relative Strength Index: \>70 (Overbought), 50-70 (Bullish), \~50 (Neutral), 30-50 (Bearish), \<30 (Oversold)  
  \- RSI between 52-67 for buying and 33-48 for selling

5\. How long to hold?  
To be checked after every buy/ sell decision. Print out the decisions/ suggestions here. No points.  
Short (Intra-day):

* Volume Spike Ratio (current volume/ avg volume): sudden interest/ manipulation  
* Cumulative Volume Delta: market aggressiveness 

Medium ()/ Long ():

* Relative Strength Index: \>70 (Overbought), 50-70 (Bullish), \~50 (Neutral), 30-50 (Bearish), \<30 (Oversold)  
* Moving Average Slope: 20 EMA (exponential moving average) (short term), 50 EMA (medium term), 200 EMA (long term) 

I have to develop an algo-trader system that consults ONLY (doesn’t trade). I want the code completely in Python. 

This will be the pipeline design.  
1\. No Main  
2\. Each of the metrics will have a separate page for processing.  It will take live data/ historical data from: wss://[stream.binance.com:9443/ws/btcusdt@trade](http://stream.binance.com:9443/ws/btcusdt@trade) . It’ll return value to questionnaires in standardized form.  
3\. Each of the metrics should be utilised by function calls from questionnaires. Each of these questionnaires need separate pages.  
4\. We’ll create a chain like this:  
Q2 is surveying every 10 minutes until minimum points are reached. After lead is generated, it calls Q1 and Q3 and passes on relevant data.  
Q3 checks parameters until minimum points are reached and keeps trying every 5 minutes until max 3 tries. After lead is generated it takes final confirmation from Q4.  
Q1 checks parameters until minimum points are reached and keeps trying every 5 minutes until max 3 tries.  
If either or both of Q3 or Q1 gets processed. Proceed to Q5.

The information should be displayed (of each and every step) on a website.  