from nba_api.stats.endpoints import boxscoretraditionalv2

# Example Game ID to inspect
game_id = '0012400059'  # Replace with a valid game ID from your games

# Step 1: Fetch individual player stats using the BoxScoreTraditionalV2 endpoint
boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
player_stats = boxscore.player_stats.get_dict()

# Step 2: Print the headers and the first player's stats for inspection
if len(player_stats['data']) > 0:
    print("Headers:", player_stats['headers'])
    print("First player data:", player_stats['data'][0])
else:
    print("No player stats found for this game.")

