import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

st.title("🏀 GameIQ")
st.subheader("NBA Analytics Dashboard")

st.write("Welcome to GameIQ!")
st.write("Explore NBA players, statistics and performance.")

all_players = players.get_active_players()

player_names = [p["full_name"] for p in all_players]

player = st.selectbox(
    "Choose a player:",
    player_names
)

st.write("You selected:", player)

selected_player = next(
    p for p in all_players if p["full_name"] == player
)

player_id = selected_player["id"]

career = playercareerstats.PlayerCareerStats(player_id=player_id)

career_df = career.get_data_frames()[0]

latest_season = career_df.iloc[-1]

season = latest_season["SEASON_ID"]
team = latest_season["TEAM_ABBREVIATION"]

st.write("Season:", season)
st.write("Team:", team)

games = latest_season["GP"]

ppg = latest_season["PTS"] / games
rpg = latest_season["REB"] / games
apg = latest_season["AST"] / games

col1, col2, col3 = st.columns(3)

col1.metric("PPG", round(ppg, 1))
col2.metric("RPG", round(rpg, 1))
col3.metric("APG", round(apg, 1))


st.write("Player ID:", player_id)

