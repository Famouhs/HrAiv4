import streamlit as st
from data.mlb import (
    get_today_games,
    get_starting_pitchers,
    get_player_stats,
    get_weather,
    get_park_factor
)
from ai.projection import project_hr_projection

# Set up Streamlit page
st.set_page_config(page_title="MLB AI HR Prop Bot", layout="wide")
st.title("⚾ MLB Daily AI Home Run Prop Bot (ML-Powered)")

# Sidebar filters
st.sidebar.header("🔍 Player/Team Filter")
player_name = st.sidebar.text_input("Search Player Name")
team_filter = st.sidebar.text_input("Filter by Team (optional)")
refresh = st.sidebar.button("🔄 Refresh Projections")

# Fetch today's games
games = get_today_games()
projections = []

# Example players (you can replace or expand this)
example_players = [
    {"id": 592450, "name": "Aaron Judge", "team": "Yankees"},
    {"id": 660271, "name": "Shohei Ohtani", "team": "Dodgers"},
]

# Loop through games
for game in games:
    game_id = game["gamePk"]
    venue = game["venue"]["name"]
    home_team = game["teams"]["home"]["team"]["name"]
    away_team = game["teams"]["away"]["team"]["name"]

    # Apply team filter if used
    if team_filter and team_filter.lower() not in (home_team + away_team).lower():
        continue

    # Get pitcher data for this game
    matchup = get_starting_pitchers(game_id)
    home_pitcher = matchup["home_pitcher"]
    away_pitcher = matchup["away_pitcher"]

    # Get weather + park context
    weather = get_weather(venue)
    park_factor = get_park_factor(venue)

    # Run projections for each player
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

# Display results
if projections:
    st.dataframe(projections, use_container_width=True)
else:
    st.info("No data yet. Try searching for a player or clicking refresh.")

