

class CoversBasketballTeamData:
    team : str = ""
    team_short : str = ""
    fg_percentage : float = 0.0
    fg_made : float = 0.0
    fg_attempted : float = 0.0
    three_percentage : float = 0.0
    three_made : float = 0.0
    three_attempted : float = 0.0
    ft_percentage : float = 0.0
    ft_made : float = 0.0
    ft_attempted : float = 0.0
    rebounds : float = 0.0
    o_rebounds : float = 0.0
    d_rebounds : float = 0.0
    assists : float = 0.0
    turnovers : float = 0.0
    assists_turnover_ratio : float = 0.0
    steals : float = 0.0
    blocks : float = 0.0
    def_fg_percentage: float = 0.0
    def_fg_made: float = 0.0
    def_fg_attempted: float = 0.0
    def_three_percentage: float = 0.0
    def_three_made: float = 0.0
    def_three_attempted: float = 0.0
    def_ft_percentage: float = 0.0
    def_ft_made: float = 0.0
    def_ft_attempted: float = 0.0
    def_rebounds: float = 0.0
    def_o_rebounds: float = 0.0
    def_d_rebounds: float = 0.0
    def_assists: float = 0.0
    def_turnovers: float = 0.0
    def_assists_turnover_ratio: float = 0.0
    def_steals: float = 0.0
    def_blocks: float = 0.0

    def __str__(self):
        result = (
        "team : " + self.team + "\n" +
        "team_short : " + self.team_short + "\n" +
        "fg% : " +str(self.fg_percentage) + "\n" +
        "fg made : " +str(self.fg_made) + "\n" +
        "fg attempted : " +str(self.fg_attempted) + "\n" +
        "reb : " +str(self.rebounds) + "\n" +
        "o_rebounds : " +str(self.o_rebounds) + "\n" +
        "d_rebounds : " + str(self.d_rebounds) + "\n" +
        "blocks : " + str(self.blocks) + "\n" +
        "steals : " + str(self.steals) + "\n" )
        return result
