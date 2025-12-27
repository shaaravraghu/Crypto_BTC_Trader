import time
from metrics import vol_24h, vol_spike, order_book_whale, sr_thresholds, bid_ask_spread

def survey_market(data_snapshot):
    """
    Q2: Sudden Interest?
    Surveys market every 10 minutes.
    Target: Collective points >= 6 to trigger Q1 and Q3.
    """
    print("DEBUG [LOGIC]: Q2 Surveying 9 metrics...")

    results = {}
    total_points = 0.0
    
    # 1. 24 Hour Trading Volume (+2 pts)
    m1 = vol_24h.process(
        data_snapshot['vol_24h'], 
        data_snapshot['vol_prev_hour']
    )
    results['vol_24h'] = m1
    total_points += m1['points']

    # 2. Volume Spike Ratio (+3 pts)
    m2 = vol_spike.process(
        data_snapshot['curr_vol'], 
        data_snapshot['avg_vol'], 
        points_to_award=3.0
    )
    results['vol_spike'] = m2
    total_points += m2['points']

    # 3. Large Order Book / Whale Activity (+2 pts)
    m3 = order_book_whale.process(
        data_snapshot['bid_vol'], 
        data_snapshot['ask_vol'], 
        points_to_award=2.0
    )
    results['whale_activity'] = m3
    total_points += m3['points']

    # 4. S/R Thresholds Proximity (+2 pts)
    m4 = sr_thresholds.process(
        data_snapshot['price'], 
        data_snapshot['sr_levels'], 
        context="Q2", 
        points_to_award=2.0
    )
    results['sr_proximity'] = m4
    total_points += m4['points']

    # 5. Bid-Ask Spread (+1 pt)
    m5 = bid_ask_spread.process(
        data_snapshot['best_bid'], 
        data_snapshot['best_ask'], 
        points_to_award=1.0
    )
    results['spread'] = m5
    total_points += m5['points']

    # Lead Generation Decision
    lead_generated = total_points >= 6
    print(f"DEBUG [LOGIC]: Q2 Analysis Complete. Total Points: {total_points}")
    

    # Return standardized form for the Web Interface
    return {
        "questionnaire": "Q2",
        "status": "Lead Generated" if lead_generated else "Surveying",
        "color": "green" if lead_generated else "blue",
        "total_points": total_points,
        "metrics_detail": results,
        "trigger_next": lead_generated
    }

def run_q2_loop(data_engine):
    """
    The orchestrator for Q2's 10-minute interval.
    In a real system, this would be managed by a task scheduler (Celery/APScheduler).
    """
    while True:
        # Get live data from the engine
        snapshot = data_engine.get_snapshot()
        
        # Process Q2
        report = survey_market(snapshot)
        
        # Logic Chain: If Q2 succeeds, call Q1 and Q3
        if report['trigger_next']:
            # Import here to avoid circular imports
            from questionnaires import q1_breakthrough, q3_aggressive
            
            # Pass the lead to the next stage
            q1_breakthrough.process_lead(snapshot)
            q3_aggressive.process_lead(snapshot)
            
        # Standardized 10-minute wait
        time.sleep(600)