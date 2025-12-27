def process(total_bid_volume: float, total_ask_volume: float, points_to_award: float):
    """
    Metric: Large Order Book (Bid/Ask) ratio for Whale Activity.
    
    Logic:
    - Ratio = Total Bid Volume / Total Ask Volume
    - Whale Short Activity: Ratio < 0.67
    - Whale Buying Activity: Ratio > 1.5
    
    Returns: (points, status, metadata)
    """
    condition_met = False
    awarded_points = 0.0
    ratio = 0.0
    activity_type = "Neutral"

    if total_ask_volume > 0:
        ratio = total_bid_volume / total_ask_volume
        
        # Check for Whale Buying Activity
        if ratio > 1.5:
            condition_met = True
            awarded_points = points_to_award
            activity_type = "Whale Buying"
            
        # Check for Whale Short Activity
        elif ratio < 0.67:
            condition_met = True
            awarded_points = points_to_award
            activity_type = "Whale Shorting"
    
    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "bid_vol": total_bid_volume,
            "ask_vol": total_ask_volume,
            "ratio": round(ratio, 4),
            "detected_activity": activity_type
        }
    }
