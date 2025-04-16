# ai/projection.py
import random

def project_hr_projection(player_stats, pitcher_stats, weather, park_factor):
    # Feature engineering example (placeholder logic)
    hr_rate = float(player_stats.get("homeRuns", 0)) / max(1, int(player_stats.get("atBats", 1)))
    wind_bonus = 0.02 if weather["wind_direction"] == "out" else -0.01
    temp_bonus = 0.01 if weather["temperature"] > 75 else 0
    park_adj = park_factor - 1.0

    prob = hr_rate + wind_bonus + temp_bonus + park_adj
    prob = min(max(prob, 0), 0.15)  # clip between 0-15%

    return {
        "probability": round(prob, 4),
        "confidence": "High" if prob > 0.1 else "Moderate" if prob > 0.05 else "Low"
    }
# ML model loader + HR probability projection logic
