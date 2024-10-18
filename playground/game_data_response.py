from nba_api.stats.endpoints import scoreboardv2, boxscoretraditionalv2
from datetime import datetime, timedelta
import json

# Function to fetch and display full response from scoreboardv2 and boxscoretraditionalv2
def inspect_endpoints(game_date):
    # Fetch scoreboard data for the provided game date
    scoreboard = scoreboardv2.ScoreboardV2(game_date=game_date)
    
    # Fetch the first game ID from the scoreboard
    games = scoreboard.get_normalized_dict()['GameHeader']
    
    if len(games) > 0:
        first_game_id = games[0]['GAME_ID']
        
        # Fetch the boxscore for the first game
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=first_game_id)
        
        # Print full scoreboard response
        print("Scoreboard Response (Game-Level Data):")
        print(json.dumps(scoreboard.get_normalized_dict(), indent=4))
        
        # Print full boxscore response
        print("\nBoxscore Response (Player-Level Data):")
        print(json.dumps(boxscore.get_normalized_dict(), indent=4))
    else:
        print(f"No games found for {game_date}.")

# Example usage:
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
inspect_endpoints(yesterday)

