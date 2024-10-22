import pandas as pd
from nba_api.stats.static import players

# Fetch all NBA players
nba_players = players.get_players()

# Create a DataFrame from the players data
players_df = pd.DataFrame(nba_players)

# Save the DataFrame to a CSV file
players_df.to_csv('nba_players.csv', index=False)

print("Player data has been successfully saved to 'nba_players.csv'.")
