
import sqlite3
import pandas as pd

url = (
    "https://github.com/sportsdataverse/"
    "sportsdataverse-data/releases/download/"
    "espn_nba_player_boxscores/"
    "player_box_2023.parquet"
)

print("Loading NBA statistics...")
df = pd.read_parquet(url)

# Keep the columns we need
df = df[
    ["game_id", "athlete_id", "season_type", "did_not_play"]
]

# Remove duplicate player-game records
df = df.drop_duplicates(
    subset=["game_id", "athlete_id"]
)

connection = sqlite3.connect("gameiq.db")
cursor = connection.cursor()

# Update existing records
records = [
    (
        int(row.season_type),
        int(row.did_not_play),
        str(row.game_id),
        int(row.athlete_id)
    )
    for row in df.itertuples(index=False)
]

cursor.executemany("""
    UPDATE player_game_stats
    SET season_type = ?,
        did_not_play = ?
    WHERE game_id = ?
      AND player_id = ?
""", records)

connection.commit()

print("Updated records:", connection.total_changes)

# Verify the update
cursor.execute("""
    SELECT season_type, COUNT(*)
    FROM player_game_stats
    GROUP BY season_type
""")

print("\nRecords by season type:")
for row in cursor.fetchall():
    print(row)

connection.close()
