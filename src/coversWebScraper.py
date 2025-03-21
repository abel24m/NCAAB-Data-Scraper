from dataclasses import dataclass
import datetime
from pathlib import Path
from time import sleep
from typing import Type, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.data.coversBasketballTeamData import CoversBasketballTeamData
from src.data.coversBasketballMatchData import BBGame, CoversBasketballMatchData, PastGames



class CoversWebScraper:

    url_date = datetime.datetime.now().strftime("%Y-%m-%d")
    ncaab_url = f"https://www.covers.com/sports/ncaab/matchups?selectedDate={url_date}"
    nba_url = f"https://www.covers.com/sports/nba/matchups?selectedDate={url_date}"
    driver = webdriver.Chrome()
    todays_date = datetime.datetime.now().strftime("%m-%d-%Y")


    def __init__(self, leagues: List[str]):
        todays_ncaab_file = Path(f"./output_files/coversScrape-NCAAB-{self.todays_date}.csv")
        todays_nba_file = Path(f"./output_files/coversScrape-NBA-{self.todays_date}.csv")
        if todays_ncaab_file.is_file() and todays_nba_file.is_file():
            print("Covers already scraped for today")
            return
        for league in leagues:
            if league == "NCAAB":
                all_ncaab_games = self.scrape_ncaab()
                f = open(f"./output_files/coversScrape-NCAAB-{self.todays_date}.csv", "w")
                for game in all_ncaab_games:
                    if game is not None:
                        line = (
                            game.home_stats.team + ", " +
                            game.away_stats.team + ", " +
                            str(game.home_point_differential) + ", " +
                            str(game.away_point_differential) + ", " +
                            str(game.total_common_opponents) + ", " + 
                            str(game.key_stats_percent_adv) + ", " +
                            str(game.more_stats_advantage) + ", " +
                            str(game.def_key_stats_percent_adv) + ", " +
                            str(game.def_more_stats_advantage) + ", " +
                            str(game.time) + "\n"
                        )
                        f.write(line)
                f.close()
            elif league == "NBA":
                all_nba_games = self.scrape_nba()
                f = open(f"./output_files/coversScrape-NBA-{self.todays_date}.csv", "w")
                for game in all_nba_games:
                    if game is not None:
                        line = (
                            game.home_stats.team + ", " +
                            game.away_stats.team + ", " +
                            str(game.home_point_differential) + ", " +
                            str(game.away_point_differential) + ", " +
                            str(game.total_common_opponents) + ", " + 
                            str(game.key_stats_percent_adv) + ", " +
                            str(game.more_stats_advantage) + ", " +
                            str(game.def_key_stats_percent_adv) + ", " +
                            str(game.def_more_stats_advantage) + ", " +
                            str(game.time) + "\n"
                        )
                        f.write(line)
                f.close()
        self.driver.quit()


    def scrape_key_stats(key_stats: BeautifulSoup, offense_team: CoversBasketballTeamData, defense_team: CoversBasketballTeamData):
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

    def scrape_more_stats(more_stats: BeautifulSoup, offense_team: CoversBasketballTeamData, defense_team: CoversBasketballTeamData):
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

    def scrape_head_to_head(hth_past: BeautifulSoup, hth: PastGames, team_one: str, team_two: str):
        records = hth_past.findAll("div", {"class" : "record-block"})
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
        past_games_table = hth_past.find("table", {"class" : "last-10-table"})

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

    def scrape_past_games(past_games_elem: BeautifulSoup, past_games : PastGames, team_name_short : str):
        records = past_games_elem.findAll("div", {"class" : "record-block"})
        if len(records) == 3 :
            # scrape all the head to head records meta data
            for record in records :
                record_label = record.find("div", {"class" : "record-label"}).text
                match record_label:
                    case "Win / Loss":
                        past_games.win_loss = record.find("div", {"class" : "record-value"}).text.strip()
                    case "ATS" :
                        past_games.ats = record.find("div", {"class" : "record-value"}).text.strip()
                    case "Over / Under" :
                        past_games.over_under = record.find("div", {"class" : "record-value"}).text.strip()

        # scrape the past individual games
        past_games_table = past_games_elem.find("table", {"class" : "last-10-table"})

        if past_games_table is not None:
            past_games_body = past_games_table.find("tbody")
            past_games_row = past_games_body.findAll("tr")
            for past_game in past_games_row:
                columns = past_game.findAll("td")
                bb_game = BBGame()
                versus_col = columns[1].text.strip()
                score_col = columns[2].text.split()
                if "@" in versus_col:
                    bb_game.home_team = versus_col.replace("@", "").strip()
                    bb_game.away_team = team_name_short
                    bb_game.home_score = int(score_col[3])
                    bb_game.away_score = int(score_col[1])
                else : 
                    bb_game.away_team = versus_col
                    bb_game.home_team = team_name_short
                    bb_game.home_score = int(score_col[1])
                    bb_game.away_score = int(score_col[3])

                past_games.past_games.append(bb_game)



    def scrape_nba(self) :
        match_href = []
        all_games = []

        # Scrape all the match hrefs from the matches page
        try:
            self.driver.get(self.nba_url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, ".pregamebox")))
            html = self.driver.page_source
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.matchup-btn-link")


            for elem in elements:
                ref = elem.get_attribute("href")
                match_href.append(ref)
        except TimeoutException:
            print("Loading Matches Page took too long")

        #Iterate through every match href. Each href is a match page
        for href in match_href:
            try:
                self.driver.get(href)
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            except TimeoutException:
                print (f"{href} could not be scraped")
                continue

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            match = CoversBasketballMatchData()

            # scrape time
            time = soup.find("span" , {"class" : "matchup-time"}).text.split()
            match.time = time[0]

            # Scrape Names of Teams and Short Names for future ref
            away_team_name = soup.find("span", {"data-team" : "away", "class" : "display-name"}).text
            home_team_name = soup.find("span", {"data-team" : "home", "class" : "display-name"}).text
            away_team_name_short = soup.find("span", {"data-team": "away", "class": "short-name"}).text
            home_team_name_short = soup.find("span", {"data-team": "home", "class": "short-name"}).text

            #Scrape Head to Head data
            head_to_head_elem = soup.find("section", {"class" : "both-team-section"})
            hth_stats = PastGames()
            CoversWebScraper.scrape_head_to_head(head_to_head_elem, hth_stats, home_team_name_short, away_team_name_short)
            match.hth_history = hth_stats

            #Scrape past games data from both teams. 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'away']").send_keys(Keys.ENTER)
            away_team_section = soup.find("section", {"class" : "away-team-section"})
            away_past_games = PastGames()
            CoversWebScraper.scrape_past_games(away_team_section, away_past_games, away_team_name_short)
            match.away_team_past = away_past_games

            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'home']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'home']").send_keys(Keys.ENTER)
            home_team_section = soup.find("section", {"class" : "home-team-section"})
            home_past_games = PastGames()
            CoversWebScraper.scrape_past_games(home_team_section, home_past_games, home_team_name_short)
            match.home_team_past = home_past_games 


            # Create Home and Away Teams assign name and short names
            away_team = CoversBasketballTeamData()
            away_team.team = away_team_name
            away_team.team_short = away_team_name_short
            home_team = CoversBasketballTeamData()
            home_team.team = home_team_name
            home_team.team_short = home_team_name_short


            away_key_stats = soup.find("section" , {"aria-labelledby" : "key-stats"})
            CoversWebScraper.scrape_key_stats(away_key_stats, away_team, home_team)
            away_more_stats = soup.find("section" , {"aria-labelledby" : "more-stats"})
            CoversWebScraper.scrape_more_stats(away_more_stats, away_team, home_team)
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href = '#home-team-offense']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[href = '#home-team-offense']").send_keys(Keys.ENTER)
            attempts = 0
            while attempts < 6:
                try:
                    WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(
                        (By.CSS_SELECTOR, "div[id = 'home-team-offense'][class = 'tab-pane fade in active']")))
                    break
                except TimeoutException:
                    print(f"home team stats never loaded for {href}")
                    attempts += 1
            if attempts == 6:
                continue
            new_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            home_key_stats = new_soup.findAll("section", {"aria-labelledby": "key-stats"})
            CoversWebScraper.scrape_key_stats(home_key_stats[1], home_team, away_team)
            home_more_stats = new_soup.findAll("section", {"aria-labelledby": "more-stats"})
            CoversWebScraper.scrape_more_stats(home_more_stats[1], home_team, away_team)
            match.home_stats = home_team
            match.away_stats = away_team
            match.analyze_key_stats()
            match.analyze_more_stats()
            match.analyze_past_games()
            all_games.append(match)
        return all_games

    def scrape_ncaab(self) :
        match_href = []
        all_games = []

        # Scrape all the match hrefs from the matches page
        try:
            self.driver.get(self.ncaab_url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, ".pregamebox")))
            html = self.driver.page_source
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.matchup-btn-link")


            for elem in elements:
                ref = elem.get_attribute("href")
                match_href.append(ref)
        except TimeoutException:
            print("Loading Matches Page took too long")

        #Iterate through every match href. Each href is a match page
        for href in match_href:
            try:
                self.driver.get(href)
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            except TimeoutException:
                print (f"{href} could not be scraped")
                continue

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            match = CoversBasketballMatchData()

            # scrape time
            time = soup.find("span" , {"class" : "matchup-time"}).text.split()
            match.time = time[0]

            # Scrape Names of Teams and Short Names for future ref
            away_team_name = soup.find("span", {"data-team" : "away", "class" : "display-name"}).text
            home_team_name = soup.find("span", {"data-team" : "home", "class" : "display-name"}).text
            away_team_name_short = soup.find("span", {"data-team": "away", "class": "short-name"}).text
            home_team_name_short = soup.find("span", {"data-team": "home", "class": "short-name"}).text

            #Scrape Head to Head data
            head_to_head_elem = soup.find("section", {"class" : "both-team-section"})
            hth_stats = PastGames()
            CoversWebScraper.scrape_head_to_head(head_to_head_elem, hth_stats, home_team_name_short, away_team_name_short)
            match.hth_history = hth_stats

            #Scrape past games data from both teams. 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'away']").send_keys(Keys.ENTER)
            away_team_section = soup.find("section", {"class" : "away-team-section"})
            away_past_games = PastGames()
            CoversWebScraper.scrape_past_games(away_team_section, away_past_games, away_team_name_short)
            match.away_team_past = away_past_games

            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'home']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'home']").send_keys(Keys.ENTER)
            home_team_section = soup.find("section", {"class" : "home-team-section"})
            home_past_games = PastGames()
            CoversWebScraper.scrape_past_games(home_team_section, home_past_games, home_team_name_short)
            match.home_team_past = home_past_games 


            # Create Home and Away Teams assign name and short names
            away_team = CoversBasketballTeamData()
            away_team.team = away_team_name
            away_team.team_short = away_team_name_short
            home_team = CoversBasketballTeamData()
            home_team.team = home_team_name
            home_team.team_short = home_team_name_short


            away_key_stats = soup.find("section" , {"aria-labelledby" : "key-stats"})
            CoversWebScraper.scrape_key_stats(away_key_stats, away_team, home_team)
            away_more_stats = soup.find("section" , {"aria-labelledby" : "more-stats"})
            CoversWebScraper.scrape_more_stats(away_more_stats, away_team, home_team)
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href = '#home-team-offense']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[href = '#home-team-offense']").send_keys(Keys.ENTER)
            attempts = 0
            while attempts < 6:
                try:
                    WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(
                        (By.CSS_SELECTOR, "div[id = 'home-team-offense'][class = 'tab-pane fade in active']")))
                    break
                except TimeoutException:
                    print(f"home team stats never loaded for {href}")
                    attempts += 1
            if attempts == 6:
                continue
            new_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            home_key_stats = new_soup.findAll("section", {"aria-labelledby": "key-stats"})
            CoversWebScraper.scrape_key_stats(home_key_stats[1], home_team, away_team)
            home_more_stats = new_soup.findAll("section", {"aria-labelledby": "more-stats"})
            CoversWebScraper.scrape_more_stats(home_more_stats[1], home_team, away_team)
            match.home_stats = home_team
            match.away_stats = away_team
            match.analyze_key_stats()
            match.analyze_more_stats()
            match.analyze_past_games()
            all_games.append(match)
        return all_games






