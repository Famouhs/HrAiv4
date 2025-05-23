# Real-time MLB API calls: schedule, stats, pitchers, weather# data/mlb.py
import requests
from datetime import datetime

BASE_URL = "https://statsapi.mlb.com/api/v1"

def get_today_games():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/schedule?sportId=1&date={today}"
    response = requests.get(url)
    games = response.json().get("dates", [])
    return games[0]["games"] if games else []

def get_starting_pitchers(game_id):
    try:
        url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
        response = requests.get(url).json()

        home_id = response["teams"]["home"]["pitchers"][0]
        away_id = response["teams"]["away"]["pitchers"][0]

        home_pitcher = response["teams"]["home"]["players"][f"ID{home_id}"]["person"]["fullName"]
        away_pitcher = response["teams"]["away"]["players"][f"ID{away_id}"]["person"]["fullName"]

        return {
            "game_id": game_id,
            "home_pitcher": home_pitcher,
            "away_pitcher": away_pitcher
        }
    except Exception as e:
        print(f"Error fetching pitchers for game {game_id}: {e}")
        return {}

        "away": teams["away"]["pitchers"][0],
        "home": teams["home"]["pitchers"][0]
    }
def get_player_stats(player_id, season="2024"):
    url = f"{BASE_URL}/people/{player_id}/stats?stats=season&season={season}&group=hitting"
    response = requests.get(url).json()
    stats = response["stats"][0]["splits"]
    return stats[0]["stat"] if stats else {}

def get_weather(venue_id):
    # NOTE: Use real weather API with key for actual data
    return {
        "temperature": 75,
        "wind_speed": 10,
        "wind_direction": "out",
        "humidity": 50
    }

def get_park_factor(venue_id):
    # Placeholder for ballpark factors — ideally scrape or use a static JSON
    park_factors = {
        1: 1.05,  # Example: Coors Field
        2: 0.98   # Example: Petco Park
    }
    return park_factors.get(venue_id, 1.00)
