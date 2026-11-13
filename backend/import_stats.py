
import pandas as pd
import sqlite3

url = (
    "https://github.com/sportsdataverse/"
    "sportsdataverse-data/releases/download/"
    "espn_nba_player_boxscores/"
    "player_box_2023.parquet"
)

print("Downloading NBA statistics...")
df = pd.read_parquet(url)

# Select the columns used by our database
columns = {
    "game_id": "game_id",
    "athlete_id": "player_id",
    "athlete_display_name": "player_name",
    "season": "season",
    "game_date": "game_date",
    "team_display_name": "team_name",
    "points": "points",
    "rebounds": "rebounds",
    "assists": "assists",
    "steals": "steals",
    "blocks": "blocks",
    "minutes": "minutes"
}

df = df[list(columns)].rename(columns=columns)

# Remove duplicate player-game records
df = df.drop_duplicates(
    subset=["game_id", "player_id"]
)

connection = sqlite3.connect("gameiq.db")

df.to_sql(
    "player_game_stats",
    connection,
    if_exists="append",
    index=False
)

connection.close()

print(f"Successfully imported {len(df)} records!")
