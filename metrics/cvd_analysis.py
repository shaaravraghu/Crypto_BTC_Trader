def process(cvd_series: list, points_to_award: float = 3.33):
    """
    Metric: Cumulative Volume Delta (CVD) Slope.
    CVD = Cumulative sum of (Buyer Volume - Seller Volume).
    
    Logic:
    - Analyzes the last 4 candles (5m timeframe).
    - Condition met if CVD is strictly increasing (Buying Aggression) 
      or strictly decreasing (Selling Aggression).
    
    Returns: (points, status, metadata)
    """
    condition_met = False
    awarded_points = 0.0
    direction = "Neutral"
    
    # We need at least 4 data points for the last 4 candles
    if len(cvd_series) >= 4:
        last_4 = cvd_series[-4:]
        
        # Check for Positive Slope (Strictly increasing)
        is_positive_slope = all(x < y for x, y in zip(last_4, last_4[1:]))
        
        # Check for Negative Slope (Strictly decreasing)
        is_negative_slope = all(x > y for x, y in zip(last_4, last_4[1:]))
        
        if is_positive_slope:
            condition_met = True
            awarded_points = points_to_award
            direction = "Aggressive Buying (Positive Slope)"
        elif is_negative_slope:
            condition_met = True
            awarded_points = points_to_award
            direction = "Aggressive Selling (Negative Slope)"

    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "cvd_last_4": [round(x, 2) for x in last_4] if len(cvd_series) >= 4 else [],
            "direction": direction,
            "observation": f"CVD trend over last 20 mins: {direction}"
        }
    }