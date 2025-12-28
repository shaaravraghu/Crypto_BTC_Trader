'''
Docstring for questionnaires.q2_interest
'''
import time
from metrics import vol_24h, vol_spike, order_book_whale, sr_thresholds, bid_ask_spread
'''
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
    '''
'''
    return {
        "questionnaire": "Q2",
        "status": "Lead Generated" if lead_generated else "Surveying",
        "color": "green" if lead_generated else "blue",
        "total_points": total_points,
        "metrics_detail": results,
        "trigger_next": lead_generated
    }
    '''

def survey_market(data_snapshot):
    print("DEBUG [LOGIC]: Q2 Surveying metrics...")
    results = {}
    total_points = 0.0
    
    try:
        # 1. 24 Hour Volume
        print("[Q2] Processing metric 1: vol_24h...")
        m1 = vol_24h.process(data_snapshot.get('vol_24h', 0), data_snapshot.get('vol_prev_hour', 0))
        results['vol_24h'] = m1
        total_points += m1.get('points', 0)
        print(f"[Q2] ✓ vol_24h complete: {m1.get('points', 0)} points")

        # 2. Volume Spike
        print("[Q2] Processing metric 2: vol_spike...")
        m2 = vol_spike.process(data_snapshot.get('curr_vol', 0), data_snapshot.get('avg_vol', 1), points_to_award=3.0)
        results['vol_spike'] = m2
        total_points += m2.get('points', 0)
        print(f"[Q2] ✓ vol_spike complete: {m2.get('points', 0)} points")

        # 3. Whale Activity
        print("[Q2] Processing metric 3: whale_activity...")
        m3 = order_book_whale.process(data_snapshot.get('bid_vol', []), data_snapshot.get('ask_vol', []), points_to_award=2.0)
        results['whale_activity'] = m3
        total_points += m3.get('points', 0)
        print(f"[Q2] ✓ whale_activity complete: {m3.get('points', 0)} points")

        # 4. S/R Thresholds
        print("[Q2] Processing metric 4: sr_thresholds...")
        m4 = sr_thresholds.process(data_snapshot.get('price', 0), data_snapshot.get('sr_levels', {}), context="Q2", points_to_award=2.0)
        results['sr_proximity'] = m4
        total_points += m4.get('points', 0)
        print(f"[Q2] ✓ sr_thresholds complete: {m4.get('points', 0)} points")

        # 5. Bid-Ask Spread
        print("[Q2] Processing metric 5: bid_ask_spread...")
        m5 = bid_ask_spread.process(data_snapshot.get('best_bid', 0), data_snapshot.get('best_ask', 0), points_to_award=1.0)
        results['spread'] = m5
        total_points += m5.get('points', 0)
        print(f"[Q2] ✓ bid_ask_spread complete: {m5.get('points', 0)} points")

    except Exception as e:
        # This will tell you if one of the Metric Modules (like vol_24h) is buggy
        print(f"❌ CRITICAL: Metric calculation failed: {e}")
        import traceback
        traceback.print_exc()
        # Return a "Safe" failing report so the orchestrator doesn't die
        return {
            "total_points": 0, 
            "trigger_next": False, 
            "metrics_detail": {},
            "status": "Error",
            "color": "red"
        }

    # Final Decision
    lead_generated = total_points >= 6
    
    # Standardized return for the Orchestrator
    result = {
        "questionnaire": "Q2",
        "total_points": total_points,
        "trigger_next": lead_generated,
        "metrics_detail": results,
        "color": "green" if lead_generated else "blue",
        "status": "Lead Generated" if lead_generated else "Surveying"
    }
    
    print(f"[Q2 COMPLETE] Status: {result['status']}, Points: {total_points}, Trigger: {lead_generated}")
    return result

