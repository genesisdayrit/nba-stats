from nba_api.stats.endpoints import boxscoretraditionalv2

# Example Game ID to inspect
game_id = '0012400059'  # Replace with a valid game ID from your games

# Step 1: Fetch individual player stats using the BoxScoreTraditionalV2 endpoint
boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
player_stats = boxscore.player_stats.get_dict()

# Step 2: Check for player data and team abbreviations
if len(player_stats['data']) > 0:
    # Extract the index of the 'TEAM_ABBREVIATION' from the headers
    headers = player_stats['headers']
    team_abbreviation_index = headers.index('TEAM_ABBREVIATION')

    # Extract all team abbreviations
    team_abbreviations = [player[team_abbreviation_index] for player in player_stats['data']]

    # Find the longest team abbreviation
    max_length_abbreviation = max(team_abbreviations, key=len)

    # Print the results
    print("Headers:", headers)
    print("First player data:", player_stats['data'][0])
    print(f"Max length team abbreviation: {max_length_abbreviation} (Length: {len(max_length_abbreviation)})")
else:
    print("No player stats found for this game.")

