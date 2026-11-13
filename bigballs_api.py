
import requests
import streamlit as st


# Get NBA player season averages
@st.cache_data(ttl=3600)
def get_nba_season_averages(player_id):
    url = (
        "https://api.bigballsdata.com/v1/nba/"
        f"players/{player_id}/season-averages"
    )

    headers = {
        "Authorization": f"Bearer {st.secrets['BIGBALLS_API_KEY']}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return response.json()["data"]


# Get NBA players
@st.cache_data(ttl=3600)
def get_nba_players():
    url = "https://api.bigballsdata.com/v1/players"

    headers = {
        "Authorization": f"Bearer {st.secrets['BIGBALLS_API_KEY']}"
    }

    params = {
        "sport": "basketball",
        "limit": 50,
        "offset": 0
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()["data"]

    return [
        player for player in data
        if player.get("league_name") == "NBA"
    ]

