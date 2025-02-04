from dataclasses import dataclass
from time import sleep
from typing import Type, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
covers_url = "https://www.covers.com"
driver.get('https://www.covers.com/sports/ncaab/matchups')
delay = 15


class CoversTeam:
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

class BBGame:
    home_team : str = ""
    away_team : str = ""
    ats_winner : str = ""
    spread : str = ""
    total : str = ""
    total_result : str = ""

class HtHHistory:
    past_games : [BBGame] = []
    win_loss : str = ""
    ats : str = ""
    over_under : str = ""


class MatchStats :

    home_stats : CoversTeam = CoversTeam()
    away_stats : CoversTeam = CoversTeam()
    hth_history : HtHHistory = HtHHistory()
    time : str = ""
    key_stats_percent_adv : float = 0.0
    key_stats_attempt_adv : float = 0.0
    more_stats_advantage : float = 0.0
    def_key_stats_percent_adv: float = 0.0
    def_key_stats_attempt_adv: float = 0.0
    def_more_stats_advantage: float = 0.0

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
        self.key_stats_percent_adv = fg_percentage_adv + three_percent_adv + ft_percent_adv
        self.key_stats_attempt_adv = fga_adv + three_attempt_adv + ft_attempt_adv
        self.def_key_stats_percent_adv = (def_fg_percentage_adv + def_three_percent_adv + def_ft_percent_adv)* (-1)
        self.def_key_stats_attempt_adv = (def_fga_adv + def_three_attempt_adv + def_ft_attempt_adv)* (-1)

    def analyze_more_stats(self):
        home_stats = self.home_stats
        away_stats = self.away_stats
        oreb_adv = float(home_stats.o_rebounds - away_stats.o_rebounds) * 1.5
        dreb_adv = float(home_stats.d_rebounds - away_stats.d_rebounds)
        assists_adv = float(home_stats.assists - away_stats.assists) * 2
        to_adv = float(home_stats.turnovers - away_stats.turnovers)
        steals_adv = float(home_stats.steals - away_stats.steals)
        blocks_adv = float(home_stats.blocks - away_stats.blocks)
        def_oreb_adv = float(home_stats.def_o_rebounds - away_stats.def_o_rebounds) * 1.5
        def_dreb_adv = float(home_stats.def_d_rebounds - away_stats.def_d_rebounds)
        def_assists_adv = float(home_stats.def_assists - away_stats.def_assists) * 2
        def_to_adv = float(home_stats.def_turnovers - away_stats.def_turnovers)
        def_steals_adv = float(home_stats.def_steals - away_stats.def_steals)
        def_blocks_adv = float(home_stats.def_blocks - away_stats.def_blocks)
        self.more_stats_advantage = oreb_adv + dreb_adv + assists_adv + to_adv + steals_adv + blocks_adv
        self.def_more_stats_advantage = (def_oreb_adv + def_dreb_adv + def_assists_adv + def_to_adv + def_steals_adv + def_blocks_adv) * -1



    def __str__(self):
        result = (
            "Home Team\t:\t" + self.home_stats.team + "\n" +
            "Away Team\t:\t" + self.away_stats.team + "\n" +
            "Key Stats Percent Advantage\t:\t" + str(self.key_stats_percent_adv) + "\n" +
            "Key Stats Attempt Advantage\t:\t" + str(self.key_stats_attempt_adv) + "\n" +
            "More Stats Advantage\t:\t" + str(self.more_stats_advantage) + "\n"
        )
        return result



def scrape_key_stats(key_stats: BeautifulSoup, offense_team: CoversTeam, defense_team: CoversTeam):
    table = key_stats.find('tbody')
    rows = table.findAll('tr')
    for row in rows:
        cols = row.findAll('span')
        stat = cols[2].text # 2 index is the stat name col
        match stat :
            case "FG%":
                offense_team.fg_percentage = float(cols[0].text)
                defense_team.def_fg_attempted = float(cols[4].text)
            case "FGM":
                offense_team.fg_made = float(cols[0].text)
                defense_team.def_fg_made = float(cols[4].text)
            case "FGA":
                offense_team.fg_attempted = float(cols[0].text)
                defense_team.def_fg_attempted = float(cols[4].text)
            case "3P%":
                offense_team.three_percentage = float(cols[0].text)
                defense_team.def_three_percentage = float(cols[4].text)
            case "3PM":
                offense_team.three_made = float(cols[0].text)
                defense_team.def_three_made = float(cols[4].text)
            case "3PA":
                offense_team.three_attempted = float(cols[0].text)
                defense_team.def_tree_attempted = float(cols[4].text)
            case "FT%":
                offense_team.ft_percentage = float(cols[0].text)
                defense_team.def_ft_percentage = float(cols[4].text)
            case "FTM":
                offense_team.ft_made = float(cols[0].text)
                defense_team.def_ft_made = float(cols[4].text)
            case "FTA":
                offense_team.ft_attempted = float(cols[0].text)
                defense_team.def_ft_attempted = float(cols[4].text)

def scrape_more_stats(more_stats: BeautifulSoup, offense_team: CoversTeam, defense_team:CoversTeam):
    table = more_stats.find('tbody')
    rows = table.findAll('tr')
    for row in rows:
        cols = row.findAll('span')
        stat = cols[2].text # 2 index is the stat name col
        match stat :
            case "REB":
                offense_team.rebounds = float(cols[0].text)
                defense_team.def_rebounds = float(cols[4].text)
            case "OREB":
                offense_team.o_rebounds = float(cols[0].text)
                defense_team.def_o_rebounds = float(cols[4].text)
            case "DREB":
                offense_team.d_rebounds = float(cols[0].text)
                defense_team.def_d_rebounds = float(cols[4].text)
            case "AST":
                offense_team.assists = float(cols[0].text)
                defense_team.def_assists = float(cols[4].text)
            case "TO":
                offense_team.turnovers = float(cols[0].text)
                defense_team.def_turnovers = float(cols[4].text)
            case "AST/TO":
                offense_team.assists_turnover_ratio = float(cols[0].text)
                defense_team.def_assists_turnover_ratio = float(cols[4].text)
            case "STL":
                offense_team.steals = float(cols[0].text)
                defense_team.def_steals = float(cols[4].text)
            case "BLK":
                offense_team.blocks = float(cols[0].text)
                defense_team.def_blocks = float(cols[4].text)

def scrape_head_to_head(hth_stats: BeautifulSoup, hth: HtHHistory, team_one: str, team_two: str):
    records = hth_stats.findAll("div", {"class" : "record-block"})
    if len(records) == 3 :
        # scrape all the head to head records meta data
        for record in records :
            record_label = record.find("div", {"class" : "record-label"}).text
            match record_label:
                case "Win / Loss":
                    hth.win_loss = record.find("div", {"class" : "record-value"}).text
                case "ATS" :
                    hth.ats = record.find("div", {"class" : "record-value"}).text
                case "Over / Under" :
                    hth.over_under = record.find("div", {"class" : "record-value"}).text
    # scrape the past individual games
    past_games_table = hth_stats.find("table", {"class" : "last-10-table"})

    if past_games_table is not None:
        past_games_body = past_games_table.find("tbody")
        past_games_row = past_games_body.findAll("tr")
        for past_game in past_games_row:
            columns = past_game.findAll("td")
            bb_game = BBGame()
            bb_game.home_team = columns[1].text.strip()
            bb_game.away_team = team_two if bb_game.home_team == team_one else team_one

            # get spread and winner
            ats_winner = columns[3].text.split()
            if (len(ats_winner) > 1):
                bb_game.ats_winner = ats_winner[0]
                bb_game.spread = ats_winner[1]
            else: # it was a push
                continue

            # get total and result
            total = columns[4].text
            if total == "P": # it was a push
                continue
            else:
                bb_game.total_result = total[:1]
                bb_game.total = total[1:]

            hth.past_games.append(bb_game)




def scrape() :
    match_href = []
    all_games = []
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "article[class = 'covers-CoversScoreboard-gameBox pre-game-box notranslate ncaab'], article[class = 'covers-CoversScoreboard-gameBox in-game-box notranslate ncaab']")))
        html = driver.page_source
        elements = driver.find_elements(By.CSS_SELECTOR, "a[class = 'matchup-btn-link'")


        for elem in elements:
            ref = elem.get_attribute("href")
            match_href.append(ref)
    except TimeoutException:
        print("Loading Matches Page took too long")

    for href in match_href:
        try:
            driver.get(href)
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
        except TimeoutException:
            print (f"{href} could not be scraped")
            continue
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        match = MatchStats()

        # scrape data and time
        time = soup.find("span" , {"class" : "matchup-time"}).text.split()
        match.time = time[0]

        # Scrape Names of Teams and Short Names for future ref
        away_team_name = soup.find("span", {"data-team" : "away", "class" : "display-name"}).text
        home_team_name = soup.find("span", {"data-team" : "home", "class" : "display-name"}).text
        away_team_name_short = soup.find("span", {"data-team": "away", "class": "short-name"}).text
        home_team_name_short = soup.find("span", {"data-team": "home", "class": "short-name"}).text

        #Scrape Head to Head data
        head_to_head_elem = soup.find("section", {"class" : "both-team-section"})
        hth_stats = HtHHistory()
        scrape_head_to_head(head_to_head_elem, hth_stats, home_team_name_short, away_team_name_short)
        match.hth_history = hth_stats

        # Create Home and Away Teams assign name and short names
        away_team = CoversTeam()
        away_team.team = away_team_name
        away_team.team_short = away_team_name_short
        home_team = CoversTeam()
        home_team.team = home_team_name
        home_team.team_short = home_team_name_short


        away_key_stats = soup.find("section" , {"aria-labelledby" : "key-stats"})
        scrape_key_stats(away_key_stats, away_team, home_team)
        away_more_stats = soup.find("section" , {"aria-labelledby" : "more-stats"})
        scrape_more_stats(away_more_stats, away_team, home_team)
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href = '#home-team-offense']")))
        driver.find_element(By.CSS_SELECTOR, "a[href = '#home-team-offense']").send_keys(Keys.ENTER)
        attempts = 0
        while attempts < 6:
            try:
                WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[id = 'home-team-offense'][class = 'tab-pane fade in active']")))
                break
            except TimeoutException:
                print(f"home team stats never loaded for {href}")
                attempts += 1
        if attempts == 6:
            continue
        new_soup = BeautifulSoup(driver.page_source, "html.parser")
        home_key_stats = new_soup.findAll("section", {"aria-labelledby": "key-stats"})
        scrape_key_stats(home_key_stats[1], home_team, away_team)
        home_more_stats = new_soup.findAll("section", {"aria-labelledby": "more-stats"})
        scrape_more_stats(home_more_stats[1], home_team, away_team)
        match.home_stats = home_team
        match.away_stats = away_team
        match.analyze_key_stats()
        match.analyze_more_stats()
        all_games.append(match)
    return all_games




def scrape_covers():
    all_ncaab_games = scrape()
    f = open("./output_files/coversScrape.csv", "w")
    for game in all_ncaab_games:
        if game is not None:
            line = (
                game.home_stats.team + ", " +
                game.away_stats.team + ", " +
                str(game.key_stats_percent_adv) + ", " +
                str(game.key_stats_attempt_adv) + ", " +
                str(game.more_stats_advantage) + ", " +
                str(game.def_key_stats_percent_adv) + ", " +
                str(game.def_key_stats_attempt_adv) + ", " +
                str(game.def_more_stats_advantage) + ", " +
                str(game.time) + "\n"
            )
            f.write(line)
    f.close()
    driver.quit()

