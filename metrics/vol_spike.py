def process(current_volume: float, average_volume: float, points_to_award: float):
    """
    Metric: Volume Spike Ratio (current volume / avg volume).
    Used to detect sudden interest or potential market manipulation.
    
    Logic:
    - Check for values > 1.5
    
    Returns: (points, status, metadata)
    """
    condition_met = False
    awarded_points = 0.0
    spike_ratio = 0.0

    # Safety check for division by zero
    if average_volume > 0:
        spike_ratio = current_volume / average_volume
        
        # Check if the ratio exceeds the 1.5 threshold
        if spike_ratio > 1.5:
            condition_met = True
            awarded_points = points_to_award
    
    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "current_volume": current_volume,
            "average_volume": average_volume,
            "spike_ratio": round(spike_ratio, 4)
        }
    }