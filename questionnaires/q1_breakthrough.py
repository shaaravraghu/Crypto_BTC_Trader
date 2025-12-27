import time
from metrics import sr_thresholds, rsi_logic, ema_slope, order_book_whale

def evaluate_breakthrough(data_snapshot, direction="buying"):
    """
    Q1: Is there a breakthrough in support/ resistance?
    Verdict >= 5 required.
    """
    results = {}
    total_points = 0.0
    
    # 1. Broken S/R Thresholds (+3 pts)
    # Check if a threshold has been breached in the past
    m1 = sr_thresholds.process(
        data_snapshot['price'], 
        data_snapshot['sr_levels'], 
        context="Q1", 
        points_to_award=3.0
    )
    results['sr_historical_breach'] = m1
    total_points += m1['points']

    # 2. Relative Strength Index (+1.5 pts)
    # Target: 52-67 for buying / 33-48 for selling
    m2 = rsi_logic.process(
        data_snapshot['rsi'], 
        context="Q1", 
        points_to_award=1.5, 
        direction=direction
    )
    results['rsi_momentum'] = m2
    total_points += m2['points']

    # 3. EMA Slope & Stack (+1.5 pts)
    # Preference: 200 EMA > 50 EMA > 20 EMA
    m3 = ema_slope.process(
        data_snapshot['ema_data'], 
        context="Q1", 
        points_to_award=1.5
    )
    results['ema_structure'] = m3
    total_points += m3['points']

    # 4. Whale Activity (+2 pts)
    m4 = order_book_whale.process(
        data_snapshot['bid_vol'], 
        data_snapshot['ask_vol'], 
        points_to_award=2.0
    )
    results['whale_activity'] = m4
    total_points += m4['points']

    # Final Verdict Logic
    # 1. Must cross 5% of threshold value (Price Check)
    # 2. Points must be >= 5
    price = data_snapshot['price']
    nearest_sr = data_snapshot['nearest_sr_value']
    price_pct_diff = abs(price - nearest_sr) / nearest_sr
    
    threshold_crossed = price_pct_diff >= 0.05
    verdict_met = (total_points >= 5) and threshold_crossed
    
    return {
        "questionnaire": "Q1",
        "status": "Breakthrough Confirmed" if verdict_met else "Testing Resistance",
        "total_points": total_points,
        "price_breach_pct": round(price_pct_diff * 100, 2),
        "success": verdict_met,
        "metrics_detail": results
    }

def process_lead(data_engine):
    """
    The retry loop for Q1.
    Tries every 5 minutes, maximum 3 times.
    """
    tries = 0
    max_tries = 3
    
    while tries < max_tries:
        tries += 1
        snapshot = data_engine.get_snapshot()
        # Note: Direction would be determined by Q2's initial findings
        report = evaluate_breakthrough(snapshot, direction="buying")
        
        # Web Interface Logging: Yellow (Processing)
        print(f"[Q1] Attempt {tries}/{max_tries} - Points: {report['total_points']}")

        if report['success']:
            # Success Color: Green
            from questionnaires import q5_hold_logic
            q5_hold_logic.generate_advice(snapshot)
            return True
        
        if tries < max_tries:
            time.sleep(300) 
            
    # Fail Color: Red
    print("[Q1] Breakthrough discarded after 3 tries.")
    return False