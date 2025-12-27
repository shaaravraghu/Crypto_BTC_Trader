import time
from metrics import vol_spike, cvd_analysis, order_book_whale, sr_thresholds, ema_slope

def evaluate_aggression(data_snapshot):
    """
    Q3 Aggressive Trading Logic.
    Ascertains market direction and checks for high-conviction points.
    Verdict >= 7 required.
    """
    results = {}
    total_points = 0.0
    
    # 1. Volume Spike Ratio (+2.5 pts)
    m1 = vol_spike.process(data_snapshot['curr_vol'], data_snapshot['avg_vol'], points_to_award=2.5)
    results['vol_spike'] = m1
    total_points += m1['points']

    # 2. Cumulative Volume Delta (+3.33 pts)
    # Checks for aggression in the last 4 candles (5m each)
    m2 = cvd_analysis.process(data_snapshot['cvd_series'], points_to_award=3.33)
    results['cvd_aggression'] = m2
    total_points += m2['points']

    # 3. Whale Activity (+2.5 pts)
    m3 = order_book_whale.process(data_snapshot['bid_vol'], data_snapshot['ask_vol'], points_to_award=2.5)
    results['whale_activity'] = m3
    total_points += m3['points']

    # 4. Broken S/R Thresholds (+2 pts)
    # Context 'Q3' checks for acceptance threshold >= 0.5%
    m4 = sr_thresholds.process(data_snapshot['price'], data_snapshot['sr_levels'], context="Q3", points_to_award=2.0)
    results['sr_break'] = m4
    total_points += m4['points']

    # 5. EMA Slope (+1.5 pts)
    m5 = ema_slope.process(data_snapshot['ema_data'], context="Q3", points_to_award=1.5)
    results['trend_slope'] = m5
    total_points += m5['points']

    verdict_met = total_points >= 7
    
    return {
        "questionnaire": "Q3",
        "verdict": "Aggressive" if verdict_met else "Wait",
        "total_points": round(total_points, 2),
        "metrics_detail": results,
        "success": verdict_met
    }

def process_lead(data_engine):
    """
    The retry loop for Q3.
    Tries every 5 minutes, maximum 3 times.
    """
    tries = 0
    max_tries = 3
    
    while tries < max_tries:
        tries += 1
        snapshot = data_engine.get_snapshot()
        report = evaluate_aggression(snapshot)
        
        # Log to Web Interface (Micro Decision)
        # Decision Color: Yellow (Processing/Retry)
        print(f"[Q3] Attempt {tries}/{max_tries} - Points: {report['total_points']}")

        if report['success']:
            # Success Color: Green
            # Proceed to Q4 for Final Confirmation
            from questionnaires import q4_efficiency
            q4_report = q4_efficiency.verify(snapshot)
            
            if q4_report['confirmed']:
                # If Q4 confirms, proceed to Q5
                from questionnaires import q5_hold_logic
                q5_hold_logic.generate_advice(snapshot)
                return True # Chain Completed Successfully
        
        # If not successful and we have tries left, wait 5 minutes
        if tries < max_tries:
            time.sleep(300) 
            
    print("[Q3] Lead Expired - Minimum points not reached after 3 tries.")
    return False