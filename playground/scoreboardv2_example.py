from nba_api.stats.endpoints import scoreboardv2
from datetime import datetime, timedelta

# Step 1: Manually set yesterday's date (2024-10-16)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Step 2: Fetch scoreboard data for October 16, 2024
scoreboard = scoreboardv2.ScoreboardV2(game_date=yesterday)

# Get the list of games from the scoreboard
games = scoreboard.get_normalized_dict()['GameHeader']

# Step 3: Print the full structure of the first game
if len(games) > 0:
    first_game = games[0]
    print("Game structure:", first_game)
else:
    print(f"No games found for {yesterday}.")

