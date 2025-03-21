import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from src.data.bovadaData import BovadaData




class BovadaWebScraper:

    ncaab_urls = ["https://www.bovada.lv/sports/basketball/college-basketball", "https://www.bovada.lv/sports/basketball/ncaa-nit"] 
    nba_url = "https://www.bovada.lv/sports/basketball/nba"
    driver = webdriver.Chrome()
    ncaab_matches = []

    def __init__(self, list_of_leagues: List[str]):
        for league in list_of_leagues:
            if league == "NCAAB":
                try:
                    self.scrape_ncaab()
                except TimeoutException:
                    print (f"Bovada NCAAB url took too much time to load!")
            elif league == "NBA":
                try:
                    delay = 15
                    self.driver.get(BovadaWebScraper.nba_url)
                    WebDriverWait(BovadaWebScraper.driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
                    self.scrape_nba()
                except TimeoutException:
                    print (f"Bovada NBA url took too much time to load!")
        BovadaWebScraper.driver.quit()
                

    def make_team_string(self, words):
        team = ""
        for word in words:
            team += word + " "
        return team.strip()

    def scrape_nba(self):
        # check if file for today already exists
        todays_date = datetime.datetime.now().strftime("%m-%d-%Y")
        todays_file = Path(f"./output_files/bovadaScrape-NBA-{todays_date}.csv")
        # if file exist then return
        if todays_file.is_file():
            print("Bovada already scraped for today")
            return
        #if not then scrape bovada
        html = self.driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        game_elements = soup.select('sp-coupon')
        f = open(f"./output_files/bovadaScrape-NBA-{todays_date}.csv", "w")

        #iterate through every row that contains a matchup
        for game in game_elements:
            date = game.find("span", {"class" : "period hidden-xs"}).text
            teams = game.findAll("span", {"class": "name"})
            home_team_words = teams[1].text.split()
            away_team_words = teams[0].text.split()
            away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
            home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
            home_team = self.make_team_string(home_team_words_cleaned)
            away_team = self.make_team_string(away_team_words_cleaned)
            spreads = game.findAll("span", {"class" : "market-line bet-handicap"})
            total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
            home_spread = spreads[1].text
            away_spread = spreads[0].text
            total = total_elem.text
            bov_ncaab_game = BovadaData(date, home_team, away_team, home_spread, away_spread, total)
            self.ncaab_matches.append(bov_ncaab_game)

            f.write((home_team + ", " + home_spread +", ").replace(chr(0xA0), ' '))
            f.write((away_team + ", " + away_spread +", ").replace(chr(0xA0), ' '))
            f.write((total + ", "))
            f.write(date.strip()+"\n")
        f.close()


    def scrape_ncaab(self):
        delay = 15
        # check if file for today already exists
        todays_date = datetime.datetime.now().strftime("%m-%d-%Y")
        todays_file = Path(f"./output_files/bovadaScrape-NCAAB-{todays_date}.csv")
        # if file exist then return
        if todays_file.is_file():
            print("Bovada already scraped for today")
            return
        f = open(f"./output_files/bovadaScrape-NCAAB-{todays_date}.csv", "w")
        for url in self.ncaab_urls:
            self.driver.get(url)
            WebDriverWait(BovadaWebScraper.driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
            html = self.driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            game_elements = soup.select('sp-coupon')
            current_date = datetime.datetime.now().strftime("%#m/%d/%y").strip()
            #iterate through every row that contains a matchup
            for game in game_elements:
                date = game.find("span", {"class" : "period hidden-xs"}).text.strip()
                date_elements = date.split()
                if date_elements[0] != current_date:
                    continue
                teams = game.findAll("span", {"class": "name"})
                home_team_words = teams[1].text.split()
                away_team_words = teams[0].text.split()
                away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
                home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
                home_team = self.make_team_string(home_team_words_cleaned)
                away_team = self.make_team_string(away_team_words_cleaned)
                spreads = game.findAll("span", {"class" : "market-line bet-handicap"})
                total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
                home_spread = spreads[1].text
                away_spread = spreads[0].text
                total = total_elem.text
                bov_ncaab_game = BovadaData(date, home_team, away_team, home_spread, away_spread, total)
                self.ncaab_matches.append(bov_ncaab_game)

                f.write((home_team + ", " + home_spread +", ").replace(chr(0xA0), ' '))
                f.write((away_team + ", " + away_spread +", ").replace(chr(0xA0), ' '))
                f.write((total + ", "))
                f.write(date.strip()+"\n")
        f.close()