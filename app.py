import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from bigballs_api import get_nba_season_averages

if st.sidebar.button("Test API Configuration"):
    if st.secrets.get("BIGBALLS_API_KEY"):
        st.sidebar.success("API key loaded successfully!")
    else:
        st.sidebar.error("API key not found.")

@st.cache_data(ttl=3600)
def get_player_stats(player_id):
    career = playercareerstats.PlayerCareerStats(
        player_id=player_id,
        timeout=15
    )
    return career.get_data_frames()[0]



st.title("🏀 GameIQ")
st.subheader("NBA Analytics Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Player Analytics",
        "Compare Players",
        "Game Centre",
        "Predictions"
    ]
)

if page == "Player Analytics":
    st.subheader("Player Analytics")

    st.write("Welcome to GameIQ!")
    st.write("Explore NBA players, statistics and performance.")

    all_players = players.get_active_players()

    player_names = [p["full_name"] for p in all_players]

    player = st.selectbox(
        "Choose a player:",
        player_names
    )

    st.header(player)

    selected_player = next(
        p for p in all_players if p["full_name"] == player
    )

    player_id = selected_player["id"]

    career = playercareerstats.PlayerCareerStats(player_id=player_id)

    career_df = career.get_data_frames()[0]

    career_df["PPG"] = career_df["PTS"] / career_df["GP"]

    season_options = career_df["SEASON_ID"].unique().tolist()

    selected_season = st.selectbox(
        "Choose a season:",
        season_options[::-1]
    )

    season_data = career_df[
        career_df["SEASON_ID"] == selected_season
    ]

    if "TOT" in season_data["TEAM_ABBREVIATION"].values:
        latest_season = season_data[
            season_data["TEAM_ABBREVIATION"] == "TOT"
        ].iloc[0]
    else:
        latest_season = season_data.iloc[-1]

    season = latest_season["SEASON_ID"]
    team = latest_season["TEAM_ABBREVIATION"]

    st.caption(f"{team} ➖ {season} Season")

    games = latest_season["GP"]

    ppg = latest_season["PTS"] / games
    rpg = latest_season["REB"] / games
    apg = latest_season["AST"] / games

    fg_pct = latest_season["FG_PCT"] * 100
    three_pct = latest_season["FQ3_PCT"] * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("PPG", round(ppg, 1))
    col2.metric("RPG", round(rpg, 1))
    col3.metric("APG", round(apg, 1))

    col4, col5, col6 = st.columns(3)

    col4.metric("FG%", f"{fg_pct: .1f}%")
    col5.metric("3P%", f"{three_pct:.1f}%")
    col6.metric("Games Played", games)

    career_df["PPG"] = career_df["PTS"] / career_df["GP"]
    career_df["APG"] = career_df["AST"] / career_df["GP"]

    st.subheader("Career Performance")

    stat_choice = st.selectbox(
        "Choose a statistic:",
        ["PPG", "RPG", "APG"]
    )

    chart_df = career_df[
        (career_df["TEAM_ABBREVIATION"] == "TOT") |
        (~career_df["SEASON_ID"].duplicated(keep=False))
    ].copy()

    st.line_chart(
        chart_df,
        x="SEASON_ID",
        y=stat_choice
    )


    st.write("Player ID:", player_id)

elif page == "Compare Players":
    st.subheader("Player Comparison")
    st.write("Compare NBA players side by side.")

    all_players = players.get_active_players()

    player_names = sorted(
        [p["full_name"] for p in all_players]
    )

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox(
            "Select Player 1:",
            player_names
        )

    with col2:
        player2 = st.selectbox(
            "Select Player 2:",
            player_names,
            index=1
        )

    selected_player1 = next(
        p for p in all_players if p["full_name"] == player1
    )

    selected_player2 = next(
        p for p in all_players if p["full_name"] == player2
    )

    player1_id = selected_player1["id"]
    player2_id = selected_player2["id"]

    try:
        df1 = get_player_stats(player1_id)
        df2 = get_player_stats(player2_id)

    except Exception:
        st.error("NBA data is temporarily unavailable. Please try again.")
        st.stop()

    for df in [df1, df2]:
        df["PPG"] = df["PTS"] / df["GP"]
        df["RPG"] = df["REB"] / df["GP"]
        df["APG"] = df["AST"] / df["GP"]

    latest1 = df1.iloc[-1]
    latest2 = df2.iloc[-1]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(player1)
        st.metric("Points Per Game", f"{latest1['PPG']:.1f}")
        st.metric("Rebounds Per Game", f"{latest1['RPG']:.1f}")
        st.metric("Assists Per Game", f"{latest1['APG']:.1f}")

    with col2:
        st.subheader(player2)
        st.metric("Points Per Game", f"{latest2['PPG']:.1f}")
        st.metric("Rebounds Per Game", f"{latest2['RPG']:.1f}")
        st.metric("Assists Per Game", f"{latest2['APG']:.1f}")

elif page == "Game Centre":
    st.subheader("NBA Game Centre")
    st.write("Upcoming games, results and match previews.")

elif page == "Predictions":
    st.subheader("GameIQ Predictions")
    st.write("Data-driven NBA predictions coming soon.")