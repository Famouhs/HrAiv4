import streamlit as st
from data.mlb import (
    get_today_games,
    get_starting_pitchers,
    get_player_stats,
    get_weather,
    get_park_factor
)
from ai.projection import project_hr_projection

# Streamlit configuration
st.set_page_config(page_title="MLB AI HR Prop Bot", layout="wide")
st.title("⚾ MLB Daily AI Home Run Prop Bot (ML-Powered)")

# Sidebar filters
st.sidebar.header("🔍 Player/Team Filter")
player_name = st.sidebar.text_input("Search Player Name")
team_filter = st.sidebar.text_input("Filter by Team (optional)")
refresh = st.sidebar.button("🔄 Refresh Projections")

# Fetch today's games and starting pitchers
games = get_today_games()
for game in games:
    pitchers = get_starting_pitchers(game["gamePk"])
# Placeholder for projection results
projections = []

# Example player list (to replace with real daily hitters later)
example_players = [
    {"id": 592450, "name": "Aaron Judge", "team": "Yankees"},
    {"id": 660271, "name": "Shohei Ohtani", "team": "Dodgers"},
]

# Loop through today’s games
for game in games:
    game_id = game["gamePk"]
    home_team = game["teams"]["home"]["team"]["name"]
    away_team = game["teams"]["away"]["team"]["name"]
    venue = game["venue"]["name"]

    matchup = next((p for p in pitchers if p["game_id"] == game_id), None)
    home_pitcher = matchup["home_pitcher"] if matchup else None
    away_pitcher = matchup["away_pitcher"] if matchup else None

    # ✅ Correct indentation
    weather = get_weather(venue)
    # Get venue data
    weather = get_weather(venue)
    park_factor = get_park_factor(venue)

    # Loop through selected players
    for player in example_players:
        if player_name and player_name.lower() not in player["name"].lower():
            continue

        stats = get_player_stats(player["id"])
        projection = project_hr_projection(
            stats,
            park_factor=park_factor,
            weather=weather
        )

        projections.append({
            "Player": player["name"],
            "Team": player["team"],
            "Opponent": f"{away_team} @ {home_team}",
            "Ballpark": venue,
            "Projected HR": projection["projected_hr"],
            "Confidence": projection["confidence"],
            "Pick": projection["pick"]
        })

# Display projections
if projections:
    st.dataframe(projections, use_container_width=True)
else:
    st.info("No results yet. Search a player or click Refresh.")
# Streamlit UI entrypoint with ML integration
