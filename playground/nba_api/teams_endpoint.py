import pandas as pd
from nba_api.stats.static import teams

# Fetch all NBA teams
nba_teams = teams.get_teams()

# Create a DataFrame from the teams data
teams_df = pd.DataFrame(nba_teams)

# Display the DataFrame
print(teams_df)
