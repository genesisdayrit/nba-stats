from nba_api.stats.endpoints import scoreboardv2, boxscoretraditionalv2
from nba_api.stats.static import teams
from datetime import datetime, timedelta

# Step 1: Manually set yesterday's date (2024-10-16)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Step 2: Fetch scoreboard data for October 16, 2024
scoreboard = scoreboardv2.ScoreboardV2(game_date=yesterday)

# Get the list of games from the scoreboard
games = scoreboard.get_normalized_dict()['GameHeader']

# Step 3: Get a list of all NBA teams for ID lookup
nba_teams = teams.get_teams()
team_id_map = {team['id']: team['full_name'] for team in nba_teams}

# Step 4: Check if there are any games from yesterday
if len(games) > 0:
    # Print game information for each game from yesterday
    for game in games:
        home_team_name = team_id_map.get(game['HOME_TEAM_ID'], 'Unknown Team')
        visitor_team_name = team_id_map.get(game['VISITOR_TEAM_ID'], 'Unknown Team')
        
        print(f"\nGame ID: {game['GAME_ID']}")
        print(f"{visitor_team_name} vs. {home_team_name}")
        print(f"Game Status: {game['GAME_STATUS_TEXT']}")
        print(f"Arena: {game['ARENA_NAME']}")

        # Step 5: Fetch individual player stats using the BoxScoreTraditionalV2 endpoint
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game['GAME_ID'])
        player_stats = boxscore.player_stats.get_dict()

        print("\nPlayer Stats:")
        for player in player_stats['data']:
            # Use correct indexes based on headers
            player_name = player[5]
            team_abbreviation = player[2]
            minutes = player[9]
            fgm = player[10]
            fga = player[11]
            fg_pct = player[12] if player[12] is not None else "N/A"
            fg3m = player[13]
            fg3a = player[14]
            fg3_pct = player[15] if player[15] is not None else "N/A"
            ftm = player[16]
            fta = player[17]
            ft_pct = player[18] if player[18] is not None else "N/A"
            oreb = player[19]
            dreb = player[20]
            reb = player[21]
            ast = player[22]
            stl = player[23]
            blk = player[24]
            turnovers = player[25]
            pf = player[26]
            pts = player[27]
            plus_minus = player[28] if player[28] is not None else "N/A"

            # Display all the stats
            print(f"{player_name} ({team_abbreviation})")
            print(f"  Minutes: {minutes}")
            print(f"  FG: {fgm}/{fga} ({fg_pct if fg_pct == 'N/A' else f'{fg_pct*100:.2f}%'})")
            print(f"  3P: {fg3m}/{fg3a} ({fg3_pct if fg3_pct == 'N/A' else f'{fg3_pct*100:.2f}%'})")
            print(f"  FT: {ftm}/{fta} ({ft_pct if ft_pct == 'N/A' else f'{ft_pct*100:.2f}%'})")
            print(f"  OREB: {oreb}, DREB: {dreb}, REB: {reb}")
            print(f"  AST: {ast}, STL: {stl}, BLK: {blk}")
            print(f"  TO: {turnovers}, PF: {pf}, PTS: {pts}")
            print(f"  Plus/Minus: {plus_minus}\n")
else:
    print(f"No games found for {yesterday}.")

