
import sqlite3

# Connect to GameIQ's database
connection = sqlite3.connect("gameiq.db")

cursor = connection.cursor()

# Create a table for NBA player game statistics
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_game_stats (
    game_id TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    player_name TEXT,
    season INTEGER,
    game_date TEXT,
    team_name TEXT,
    points REAL,
    rebounds REAL,
    assists REAL,
    steals REAL,
    blocks REAL,
    minutes REAL,
    PRIMARY KEY (game_id, player_id)
)
""")

connection.commit()
connection.close()

print("GameIQ database created successfully!")


# Add extra columns to our existing database
connection = sqlite3.connect("gameiq.db")
cursor = connection.cursor()

for column, data_type in [
    ("season_type", "INTEGER"),
    ("did_not_play", "INTEGER")
]:
    try:
        cursor.execute(
            f"ALTER TABLE player_game_stats "
            f"ADD COLUMN {column} {data_type}"
        )
        print(f"Added column: {column}")

    except sqlite3.OperationalError as error:
        if "duplicate column name" in str(error):
            print(f"Column already exists: {column}")
        else:
            raise

connection.commit()
connection.close()

print("Database structure updated successfully!")
