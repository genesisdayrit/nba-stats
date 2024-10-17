from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

# Define a formatted output for game info
game_format = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}"

# Fetch today's scoreboard data
board = scoreboard.ScoreBoard()
print(f"ScoreBoardDate: {board.score_board_date}")

# Iterate through the games and display them with local time
games = board.games.get_dict()
for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(game_format.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))

