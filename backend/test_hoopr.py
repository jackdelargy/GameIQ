
import requests

url = (
    "https://api.github.com/repos/"
    "sportsdataverse/sportsdataverse-data/"
    "releases/tags/espn_nba_player_boxscores"
)

response = requests.get(url, timeout=30)
response.raise_for_status()

assets = response.json()["assets"]

seasons = []

for asset in assets:
    name = asset["name"]

    if name.startswith("player_box_") and name.endswith(".parquet"):
        year = name.replace("player_box_", "").replace(".parquet", "")
        seasons.append(year)

print("Available NBA season-ending years:")
print(sorted(seasons))

print("\nTotal seasons:", len(seasons))
