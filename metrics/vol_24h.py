def process(current_24h_volume: float, previous_hour_volume: float):
    """
    Metric: 24 Hour Trading Volume logic for Q2.
    Check for 50% increase in volume as compared to previous hour.
    
    Returns: (points, status, metadata)
    """
    points_possible = 2
    points_awarded = 0
    condition_met = False
    
    # Avoid division by zero if the previous hour had no volume
    if previous_hour_volume > 0:
        # Calculate percentage increase
        increase_ratio = (current_24h_volume - previous_hour_volume) / previous_hour_volume
        
        # Check for 50% increase (0.50)
        if increase_ratio >= 0.50:
            points_awarded = points_possible
            condition_met = True
    else:
        increase_ratio = 0.0

    # Standardized Return Format
    return {
        "points": points_awarded,
        "status": condition_met,
        "raw_value": {
            "current_24h_vol": current_24h_volume,
            "prev_hour_vol": previous_hour_volume,
            "increase_pct": round(increase_ratio * 100, 2)
        }
    }
