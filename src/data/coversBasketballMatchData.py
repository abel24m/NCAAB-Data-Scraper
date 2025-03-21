
from typing import List
from src.data.coversBasketballTeamData import CoversBasketballTeamData


class BBGame:
    home_team : str = ""
    away_team : str = ""
    ats_winner : str = ""
    home_score : int = 0
    away_score : int = 0
    spread : str = ""
    total : str = ""
    total_result : str = ""

class PastGames:
    past_games : List[BBGame]
    win_loss : str 
    ats : str
    over_under : str 

    def __init__(self):
        self.past_games = []
        self.win_loss = ""
        self.ats = ""
        self.over_under = ""

    def __str__(self):
        result = (
            "Home Team\t:\t" + self.home_stats.team + "\n" +
            "Away Team\t:\t" + self.away_stats.team + "\n" +
            "Key Stats Percent Advantage\t:\t" + str(self.key_stats_percent_adv) + "\n" +
            "Key Stats Attempt Advantage\t:\t" + str(self.key_stats_attempt_adv) + "\n" +
            "More Stats Advantage\t:\t" + str(self.more_stats_advantage) + "\n"
        )
        return result


class CoversBasketballMatchData :

    home_stats : CoversBasketballTeamData = CoversBasketballTeamData()
    away_stats : CoversBasketballTeamData = CoversBasketballTeamData()
    hth_history : PastGames = PastGames()
    home_team_past : PastGames = PastGames()
    away_team_past : PastGames = PastGames()
    time : str = ""
    key_stats_percent_adv : float = 0.0
    key_stats_attempt_adv : float = 0.0
    more_stats_advantage : float = 0.0
    def_key_stats_percent_adv: float = 0.0
    def_key_stats_attempt_adv: float = 0.0
    def_more_stats_advantage: float = 0.0
    home_point_differential : float = 0.0
    away_point_differential : float = 0.0
    total_common_opponents : int = 0
    home_pd_opps : list[str]
    away_pd_opps : list[str]

    def analyze_key_stats(self):
        home_stats = self.home_stats
        away_stats = self.away_stats
        fg_percentage_adv = float(home_stats.fg_percentage - away_stats.fg_percentage) * 2
        fga_adv = float(home_stats.fg_attempted - away_stats.fg_attempted) * 2
        three_percent_adv = float(home_stats.three_percentage - away_stats.three_percentage) * 3
        three_attempt_adv = float(home_stats.three_attempted - away_stats.three_attempted) * 3
        ft_percent_adv = float(home_stats.ft_percentage - away_stats.ft_percentage)
        ft_attempt_adv = float(home_stats.ft_attempted - away_stats.ft_attempted)
        def_fg_percentage_adv = float(home_stats.def_fg_percentage - away_stats.def_fg_percentage) * 2
        def_fga_adv = float(home_stats.def_fg_attempted - away_stats.def_fg_attempted) * 2
        def_three_percent_adv = float(home_stats.def_three_percentage - away_stats.def_three_percentage) * 3
        def_three_attempt_adv = float(home_stats.def_three_attempted - away_stats.def_three_attempted) * 3
        def_ft_percent_adv = float(home_stats.def_ft_percentage - away_stats.def_ft_percentage)
        def_ft_attempt_adv = float(home_stats.def_ft_attempted - away_stats.def_ft_attempted)
        self.key_stats_percent_adv = (fg_percentage_adv + three_percent_adv + ft_percent_adv) / 3.0
        self.key_stats_attempt_adv = fga_adv + three_attempt_adv + ft_attempt_adv
        self.def_key_stats_percent_adv = ((def_fg_percentage_adv + def_three_percent_adv + def_ft_percent_adv)* (-1)) / 3.0
        self.def_key_stats_attempt_adv = (def_fga_adv + def_three_attempt_adv + def_ft_attempt_adv)* (-1)

    def analyze_more_stats(self):
        home_stats = self.home_stats
        away_stats = self.away_stats
        oreb_adv = float(home_stats.o_rebounds - away_stats.o_rebounds) * 1.5
        dreb_adv = float(home_stats.d_rebounds - away_stats.d_rebounds)
        assists_adv = float(home_stats.assists - away_stats.assists) * 1.5 
        to_adv = float(home_stats.turnovers - away_stats.turnovers) * 1.5
        steals_adv = float(home_stats.steals - away_stats.steals)
        blocks_adv = float(home_stats.blocks - away_stats.blocks)
        def_oreb_adv = float(home_stats.def_o_rebounds - away_stats.def_o_rebounds) * 1.5
        def_dreb_adv = float(home_stats.def_d_rebounds - away_stats.def_d_rebounds) 
        def_assists_adv = float(home_stats.def_assists - away_stats.def_assists) * 1.5
        def_to_adv = float(home_stats.def_turnovers - away_stats.def_turnovers) * 1.5
        def_steals_adv = float(home_stats.def_steals - away_stats.def_steals)
        def_blocks_adv = float(home_stats.def_blocks - away_stats.def_blocks)
        self.more_stats_advantage = (oreb_adv + dreb_adv + assists_adv + to_adv + steals_adv + blocks_adv) / 6.0
        self.def_more_stats_advantage = ((def_oreb_adv + def_dreb_adv + def_assists_adv + def_to_adv + def_steals_adv + def_blocks_adv) * -1) / 6.0

    def analyze_past_games(self):
        home_short_name = self.home_stats.team_short
        away_short_name = self.away_stats.team_short
        list_of_common_opponents = []
        list_home_pointdiff_opponents = []
        list_away_pointdiff_opponents = []
        home_pointdiff_games = 0
        away_pointdiff_games = 0
        home_point_diff = 0
        away_point_diff = 0
        #iterate through every past game from the home team
        for home_past_game in self.home_team_past.past_games:
            #find the opponent for the game
            home_team = home_past_game.home_team
            away_team = home_past_game.away_team
            opponent = ""
            #if the home team is the current team then the opponent is the away team
            #if its not then the home team is the opponent
            if home_team == home_short_name:
                opponent = away_team
                matchup_home_scorediff = home_past_game.home_score - home_past_game.away_score
            else :
                opponent = home_team
                matchup_home_scorediff = home_past_game.away_score - home_past_game.home_score
            #if opponent has already been played before continue or if the opponent is the same as the current one. 
            if opponent in list_of_common_opponents or opponent == away_short_name:
                continue
            # find if the away team has a common oppponent from their past games
            matchup_away_scorediff = None
            for away_past_game in self.away_team_past.past_games:
                home_team = away_past_game.home_team
                away_team = away_past_game.away_team
                if opponent == home_team or opponent == away_team:
                    list_of_common_opponents.append(opponent)
                    if opponent == home_team:
                        matchup_away_scorediff = away_past_game.away_score - away_past_game.home_score
                        break
                    else :
                        matchup_away_scorediff = away_past_game.home_score - away_past_game.home_score
                        break
            if matchup_away_scorediff is not None and matchup_home_scorediff is not None:
                if matchup_home_scorediff > matchup_away_scorediff:
                    list_home_pointdiff_opponents.append(opponent)
                    home_pointdiff_games += 1
                    home_point_diff += matchup_home_scorediff - matchup_away_scorediff
                elif matchup_away_scorediff > matchup_home_scorediff:
                    list_away_pointdiff_opponents.append(opponent)
                    away_pointdiff_games += 1
                    away_point_diff += matchup_away_scorediff - matchup_home_scorediff
        self.total_common_opponents = len(list_of_common_opponents)
        if home_pointdiff_games > 0:
            self.home_point_differential = home_point_diff / float(home_pointdiff_games)
            self.home_pd_opps = list_home_pointdiff_opponents
        if away_pointdiff_games > 0 :
            self.away_point_differential = away_point_diff / float(away_pointdiff_games)
            self.away_pd_opps = list_away_pointdiff_opponents
        
        






    def __str__(self):
        result = (
            "Home Team\t:\t" + self.home_stats.team + "\n" +
            "Away Team\t:\t" + self.away_stats.team + "\n" +
            "Key Stats Percent Advantage\t:\t" + str(self.key_stats_percent_adv) + "\n" +
            "Key Stats Attempt Advantage\t:\t" + str(self.key_stats_attempt_adv) + "\n" +
            "More Stats Advantage\t:\t" + str(self.more_stats_advantage) + "\n"
        )
        return result