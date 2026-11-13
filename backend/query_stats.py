
import sqlite3


import sqlite3

connection = sqlite3.connect("gameiq.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT
        player_name,
        COUNT(*) AS games,
        ROUND(AVG(points), 1) AS ppg,
        ROUND(AVG(rebounds), 1) AS rpg,
        ROUND(AVG(assists), 1) AS apg
    FROM player_game_stats
    WHERE player_name = 'Stephen Curry'
      AND season_type = 2
      AND did_not_play = 0
    GROUP BY player_name
""")

result = cursor.fetchone()

print("Stephen Curry - 2022-23 Regular Season")
print(result)

connection.close()

