def process(best_bid: float, best_ask: float, points_to_award: float):
    """
    Metric: Bid-Ask Spread percentage.
    Indicates liquidity and the hidden cost of immediate execution.
    
    Logic:
    - Spread % = ((Ask - Bid) / Ask) * 100
    - Favorable: Spread < 0.3%
    
    Returns: (points, status, metadata)
    """
    condition_met = False
    awarded_points = 0.0
    spread_pct = 0.0

    if best_ask > 0:
        # Calculate the percentage spread
        spread_pct = ((best_ask - best_bid) / best_ask) * 100
        
        # Check against the 0.3% threshold
        if spread_pct < 0.3:
            condition_met = True
            awarded_points = points_to_award
            
    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread_pct": round(spread_pct, 4),
            "threshold": 0.3
        }
    }
