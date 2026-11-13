
import pandas as pd

url = (
    "https://github.com/sportsdataverse/"
    "sportsdataverse-data/releases/download/"
    "espn_nba_player_boxscores/"
    "player_box_2027.parquet"
)

try:
    df = pd.read_parquet(url)

    print("2026-27 NBA season")
    print("Total records:", len(df))

    if not df.empty:
        print("Earliest game:", df["game_date"].min())
        print("Latest game:", df["game_date"].max())
        print("Unique games:", df["game_id"].nunique())
    else:
        print("The file currently contains no records.")

except Exception as error:
    print("Error:", error)
