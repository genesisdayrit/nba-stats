import pandas as pd
from nba_api.stats.static import players

# Fetch all NBA players
nba_players = players.get_players()

# Create a DataFrame from the players data
players_df = pd.DataFrame(nba_players)

# Display the DataFrame
print(players_df)
