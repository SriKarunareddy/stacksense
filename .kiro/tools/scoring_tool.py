def score_technology(tech, constraints):
    score = 0
    explanation = []

    if constraints["team_size"] <= 5 and tech["ease_of_use"] == "high":
        score += 3
        explanation.append("Easy to use for small teams")

    if constraints["budget"] == "low" and tech["cost"] == "low":
        score += 3
        explanation.append("Fits low budget constraints")

    if constraints["scalability"] == "high" and tech["scalability"] == "high":
        score += 4
        explanation.append("Scales well for future growth")

    if constraints["time_to_market"] == "fast" and tech["development_speed"] == "fast":
        score += 3
        explanation.append("Faster time to market")

    return score, explanation
