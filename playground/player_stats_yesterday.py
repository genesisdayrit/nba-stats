import csv
from nba_api.stats.endpoints import scoreboardv2, boxscoretraditionalv2
from nba_api.stats.static import teams
from datetime import datetime, timedelta

# Function to fetch player stats and write to CSV
def extract_player_stats_to_csv(game_date, csv_file_path):
    # Fetch scoreboard data for the provided game date
    scoreboard = scoreboardv2.ScoreboardV2(game_date=game_date)
    
    # Get the list of games from the scoreboard
    games = scoreboard.get_normalized_dict()['GameHeader']
    
    # Get a list of all NBA teams for ID lookup
    nba_teams = teams.get_teams()
    team_id_map = {team['id']: team['full_name'] for team in nba_teams}
    
    # Prepare a list to collect all player stats
    player_game_stats = []
    
    # Check if there are any games from the provided date
    if len(games) > 0:
        # Fetch player stats for each game
        for game in games:
            game_id = game['GAME_ID']
            boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            player_stats = boxscore.player_stats.get_dict()
            
            # Append each player's stats to the list
            for player in player_stats['data']:
                player_game_stats.append(player)
    
    # Write the stats to a CSV file
    headers = player_stats['headers']
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(player_game_stats)  # Write player data
    
    print(f"Player stats extracted to: {csv_file_path}")

# Example usage:
# Set the date (e.g., yesterday)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Set the output CSV file path
csv_output_path = 'player_game_stats.csv'

# Call the function to extract stats and write to CSV
extract_player_stats_to_csv(yesterday, csv_output_path)

