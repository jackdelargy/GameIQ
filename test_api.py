
from bigballs_api import get_nba_players, get_nba_season_averages

try:
    players = get_nba_players()

    print("NBA players found:", len(players))

    for player in players:
        print(player["name"], "-", player["id"])

    if players:
        player = players[0]

        print("\nTesting season averages for:", player["name"])

        stats = get_nba_season_averages(player["id"])

        print("Seasons returned:", len(stats))

        for season in stats:
            print(
                season["season"],
                "PPG:", season["pts"],
                "RPG:", season["reb"],
                "APG:", season["ast"]
            )

except Exception as error:
    print("API test failed:", error)

