import sqlite3
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(
    title="GameIQ API",
    description="NBA analytics and statistics backend",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to GameIQ!",
        "status": "running",
        "version": "0.1.0"
    }


players = [
    {
        "id": 2544,
        "name": "LeBron James",
        "team": "Los Angeles Lakers"
    },
    {
        "id": 201939,
        "name": "Stephen Curry",
        "team": "Golden State Warriors"
    },
    {
        "id": 1630162,
        "name": "Anthony Edwards",
        "team": "Minnesota Timberwolves"
    }
]


@app.get("/players")
def get_players():
    return players


from fastapi import HTTPException

@app.get("/players/{player_id}")
def get_player(player_id: int):
    for player in players:
        if player["id"] == player_id:
            return player

    raise HTTPException(
        status_code=404,
        detail="Player not found"
    )


# Locate our database
DB_PATH = Path(__file__).resolve().parent / "gameiq.db"


@app.get("/players/{player_id}/stats")
def get_player_stats(player_id: int):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                player_id,
                player_name,
                season,
                COUNT(*) AS games,
                ROUND(AVG(points), 1) AS ppg,
                ROUND(AVG(rebounds), 1) AS rpg,
                ROUND(AVG(assists), 1) AS apg
            FROM player_game_stats
            WHERE player_id = ?
              AND season_type = 2
              AND did_not_play = 0
            GROUP BY player_id, player_name, season
        """, (player_id,))

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Player statistics not found"
            )

        return dict(result)

    finally:
        connection.close()
