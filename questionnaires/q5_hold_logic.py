from metrics import vol_spike, cvd_analysis, rsi_logic, ema_slope

def generate_advice(data_snapshot):
    """
    Q5: How long to hold?
    Triggered after a buy/sell decision from Q1 or Q3/Q4.
    Provides duration-based suggestions based on volatility and trend structure.
    """
    print(f"Q5: generate_advice started — timestamp={data_snapshot.get('timestamp')} price={data_snapshot.get('price')}")
    # 1. Short (Intra-day) Analysis
    # Uses Volume Spike and CVD to check immediate momentum
    m_spike = vol_spike.process(data_snapshot['curr_vol'], data_snapshot['avg_vol'], 0)
    m_cvd = cvd_analysis.process(data_snapshot['cvd_series'], 0)
    
    short_term_advice = "STABILIZING"
    if m_spike['status'] and m_cvd['status']:
        short_term_advice = "HIGH AGGRESSION: Suitable for scalp/intra-day momentum."
    elif m_cvd['status']:
        short_term_advice = "MODERATE AGGRESSION: Watch for CVD exhaustion."
    else:
        short_term_advice = "LOW MOMENTUM: Tighten stop-losses for intra-day."

    # 2. Medium/Long Term Analysis
    # Uses RSI and EMA Slope to check structural health
    m_rsi = rsi_logic.process(data_snapshot['rsi'], context="Q5", points_to_award=0)
    m_ema = ema_slope.process(data_snapshot['ema_data'], context="Q5", points_to_award=0)
    
    # Extract structural info
    is_bullish = m_rsi['raw_value']['sentiment'] == "Bullish"
    is_aligned = m_ema['raw_value']['alignment'] == "True" # 200 > 50 > 20
    
    med_long_advice = "CAUTION"
    if is_bullish and is_aligned:
        med_long_advice = "STRONG STRUCTURE: Trend supports multi-day holding."
    elif is_bullish or is_aligned:
        med_long_advice = "TRANSITIONAL: Moderate conviction for medium term."
    else:
        short_term_advice = "WEAK STRUCTURE: Long-term trend is bearish/uncertain."

    # Formatting the Decision/Suggestion Output
    decision_report = {
        "questionnaire": "Q5",
        "timestamp": data_snapshot.get('timestamp'),
        "verdict_summary": {
            "Short_Term": short_term_advice,
            "Medium_Long_Term": med_long_advice
        },
        "raw_metrics_snapshot": {
            "RSI_Sentiment": m_rsi['raw_value']['sentiment'],
            "CVD_Direction": m_cvd['raw_value']['direction'],
            "EMA_Slope_20": m_ema['raw_value']['slopes']['20']
        },
        "color": "purple" # Specific color for the Final Advice step
    }

    print("Q5: final advice prepared")
    
    print(f"[Q5 COMPLETE] Advice Generated - Short: {short_term_advice[:50]}..., Long: {med_long_advice[:50]}...")
    
    # Print to console for the 'consultant' view
    print("\n--- FINAL TRADING CONSULTATION ---")
    print(f"SHORT TERM: {short_term_advice}")
    print(f"MED/LONG TERM: {med_long_advice}")
    print("----------------------------------\n")

    return decision_report