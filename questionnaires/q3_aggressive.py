import time
from metrics import vol_spike, cvd_analysis, order_book_whale, sr_thresholds, ema_slope

def evaluate_aggression(data_snapshot):
    """
    Q3 Aggressive Trading Logic.
    Ascertains market direction and checks for high-conviction points.
    Verdict >= 7 required.
    """
    print(f"Q3: evaluate_aggression called — price={data_snapshot.get('price')}")
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
    
    result = {
        "questionnaire": "Q3",
        "verdict": "Aggressive" if verdict_met else "Wait",
        "total_points": round(total_points, 2),
        "metrics_detail": results,
        "success": verdict_met
    }
    
    print(f"[Q3 COMPLETE] Verdict: {result['verdict']}, Points: {total_points}, Success: {verdict_met}")
    return result
