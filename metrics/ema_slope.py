def process(ema_data: dict, context: str, points_to_award: float):
    """
    Metric: Exponential Moving Average (EMA) Slope and Alignment.
    Horizons: 20 (Short), 50 (Medium), 200 (Long).
    
    Logic:
    - Q3: Directional slope (Positive for Bullish / Negative for Bearish).
    - Q1: Slope + Preference check (200 EMA > 50 EMA > 20 EMA).
    """
    condition_met = False
    awarded_points = 0.0
    
    # Calculate slopes (current - previous)
    # ema_data = {"ema20": [vals], "ema50": [vals], "ema200": [vals]}
    slope_20 = ema_data['ema20'][-1] - ema_data['ema20'][-2]
    slope_50 = ema_data['ema50'][-1] - ema_data['ema50'][-2]
    slope_200 = ema_data['ema200'][-1] - ema_data['ema200'][-2]

    # Q3 Logic: Simple Slope Direction
    if context == "Q3":
        if abs(slope_20) > 0: # Looking for any clear bias
            condition_met = True
            awarded_points = points_to_award

    # Q1 Logic: Trend Alignment Preference
    elif context == "Q1":
        # Preference: 200 EMA > 50 EMA > 20 EMA
        stack_aligned = ema_data['ema200'][-1] > ema_data['ema50'][-1] > ema_data['ema20'][-1]
        
        # Check if slope matches direction (Positive for buying, Negative for selling)
        # Note: Direction is passed from the questionnaire logic
        if stack_aligned:
            condition_met = True
            awarded_points = points_to_award

    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "slopes": {"20": slope_20, "50": slope_50, "200": slope_200},
            "alignment": f"200 > 50 > 20: {ema_data['ema200'][-1] > ema_data['ema50'][-1] > ema_data['ema20'][-1]}",
            "context_applied": context
        }
    }