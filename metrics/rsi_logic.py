def process(rsi_value: float, context: str, points_to_award: float, direction: str = "buying"):
    """
    Metric: Relative Strength Index (RSI).
    
    Logic:
    - Overbought (>70), Bullish (50-70), Neutral (~50), Bearish (30-50), Oversold (<30).
    - Q1/Q4 Target: 52-67 for Buying and 33-48 for Selling.
    """
    condition_met = False
    awarded_points = 0.0
    sentiment = "Neutral"

    # Define Sentiment Categories
    if rsi_value > 70: sentiment = "Overbought"
    elif 50 < rsi_value <= 70: sentiment = "Bullish"
    elif 30 <= rsi_value <= 50: sentiment = "Bearish"
    elif rsi_value < 30: sentiment = "Oversold"

    # Q1 and Q4 Logic: Momentum Corridors
    if context in ["Q1", "Q4"]:
        if direction == "buying" and 52 <= rsi_value <= 67:
            condition_met = True
            awarded_points = points_to_award
        elif direction == "selling" and 33 <= rsi_value <= 48:
            condition_met = True
            awarded_points = points_to_award

    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "rsi_value": round(rsi_value, 2),
            "sentiment": sentiment,
            "in_momentum_zone": condition_met,
            "target_direction": direction
        }
    }