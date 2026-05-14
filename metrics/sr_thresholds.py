def process(current_price: float, sr_levels: dict, context: str, points_to_award: float):
    """
    Metric: Support/Resistance Thresholds for multiple time horizons.
    Horizons: Short (7/14d), Medium (30/90d), Long (180/365d).
    
    Logic per Context:
    - Q2: Is price within 1% of any threshold? (+2 pts)
    - Q3: Is price > 0.5% beyond a broken threshold? (+2 pts)
    - Q1: Has a threshold been breached at least once in history? (+3 pts)
    """
    condition_met = False
    awarded_points = 0.0
    details = []

    # sr_levels expected format: {"7d": {"sup": val, "res": val, "breached": bool}, ...}

    for period, levels in sr_levels.items():
        support = levels['sup']
        resistance = levels['res']
        
        # Q2 Logic: Proximity (Sudden Interest)
        if context == "Q2":
            prox_s = abs(current_price - support) / support
            prox_r = abs(current_price - resistance) / resistance
            if prox_s < 0.01 or prox_r < 0.01:
                condition_met = True
                details.append(f"{period} Proximity detected")

        # Q3 Logic: Broken Acceptance (Aggressive Trading)
        elif context == "Q3":
            # Check if price has pushed 0.5% past support (down) or resistance (up)
            if current_price > (resistance * 1.005) or current_price < (support * 0.995):
                condition_met = True
                details.append(f"{period} Break confirmed (>0.5%)")

        # Q1 Logic: Historical Breach (Breakthrough)
        elif context == "Q1":
            if levels.get('breached', False):
                condition_met = True
                details.append(f"{period} Historical breach found")

    if condition_met:
        awarded_points = points_to_award

    return {
        "points": awarded_points,
        "status": condition_met,
        "raw_value": {
            "current_price": current_price,
            "logic_applied": context,
            "observations": details,
            "levels_analyzed": list(sr_levels.keys())
        }
    }
