from metrics import turnover_ratio, bid_ask_spread, rsi_logic

def verify(data_snapshot, direction="buying"):
    """
    Q4: Current trading efficiency?
    Final confirmation for Aggressive Trading (Q3).
    Verdict >= 2 required.
    """
    results = {}
    total_points = 0.0

    # 1. Turnover Ratio (+2 points)
    # Measures how much of the asset supply is moving
    m1 = turnover_ratio.process(
        data_snapshot['vol_24h'], 
        data_snapshot['market_cap'], 
        points_to_award=2.0
    )
    results['turnover_efficiency'] = m1
    total_points += m1['points']

    # 2. Bid-Ask Spread (+1.5 points)
    # Target: < 0.3% for high liquidity
    m2 = bid_ask_spread.process(
        data_snapshot['best_bid'], 
        data_snapshot['best_ask'], 
        points_to_award=1.5
    )
    results['liquidity_spread'] = m2
    total_points += m2['points']

    # 3. RSI Momentum Corridor (+0.5 points)
    # Target: 52-67 (buying) / 33-48 (selling)
    m3 = rsi_logic.process(
        data_snapshot['rsi'], 
        context="Q4", 
        points_to_award=0.5, 
        direction=direction
    )
    results['momentum_alignment'] = m3
    total_points += m3['points']

    # Final Verification Decision
    is_confirmed = total_points >= 2
    
    return {
        "questionnaire": "Q4",
        "confirmed": is_confirmed,
        "total_points": total_points,
        "metrics_detail": results,
        "color": "green" if is_confirmed else "red",
        "status": "Efficiency Verified" if is_confirmed else "Low Efficiency - Lead Blocked"
    }