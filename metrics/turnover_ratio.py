def process(volume: float, market_cap: float, points_to_award: float = 2.0):
    """
    Metric: Turnover Ratio (Volume / Market Cap).
    Measures how efficiently the asset is being traded relative to its size.
    
    Logic:
    - High turnover indicates strong liquid interest.
    - Used in Q4 to confirm if the current 'Aggressive Trading' lead is efficient.
    
    Returns: (points, status, metadata)
    """
    condition_met = False
    awarded_points = 0.0
    turnover_ratio = 0.0

    if market_cap > 0:
        turnover_ratio = volume / market_cap
        
        # In a consultant system, any measurable turnover during a lead
        # is considered a positive efficiency sign. 
        # For BTC, typical daily turnover is 0.02 - 0.05 (2-5%).
        if turnover_ratio > 0:
            condition_met = True
            awarded_points = points_to_award

    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "volume": volume,
            "market_cap": market_cap,
            "turnover_ratio": round(turnover_ratio, 6),
            "efficiency_multiplier": "High" if turnover_ratio > 0.03 else "Standard"
        }
    }