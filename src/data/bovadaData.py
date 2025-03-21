



class BovadaData:

    date: str
    home_team: str
    away_team: str
    home_spread: str
    away_spread: str
    total: str

    def __init__(self, date: str, home_team: str, away_team: str, home_spread: str, away_spread: str, total: str):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_spread = home_spread
        self.away_spread = away_spread
        self.total = total

