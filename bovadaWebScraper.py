from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def make_team_string(words):
    team = ""
    for word in words:
        team += word + " "
    return team.strip()


def scrape_bovada():
    driver = webdriver.Chrome()
    driver.get('https://www.bovada.lv/sports/basketball/college-basketball')
    delay = 15
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        game_elements = soup.select('sp-coupon')
        f = open("./output_files/bovadaOdds.txt", "w")
        for game in game_elements:
            date = game.find("span", {"class" : "period hidden-xs"}).text
            teams = game.findAll("span", {"class": "name"})
            home_team_words = teams[0].text.split()
            away_team_words = teams[1].text.split()
            away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
            home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
            home_team = make_team_string(home_team_words_cleaned)
            away_team = make_team_string(away_team_words_cleaned)
            spreads = game.findAll("span", {"class" : "market-line bet-handicap"})
            odds = game.findAll("span", {"class" : "bet-price"})
            total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
            home_spread = spreads[0].text
            away_spread = spreads[1].text
            home_odds = odds[0].text
            away_odds = odds[1].text
            total = total_elem.text
            home_spread_odds = home_spread + "\t" + home_odds.strip()
            away_spread_odds = away_spread + "\t" + away_odds.strip()
            f.write((home_team + "\t" + home_spread_odds +"\n").replace(chr(0xA0), ' '))
            f.write((away_team + "\t" + away_spread_odds +"\n").replace(chr(0xA0), ' '))
            f.write((total + "\n"))
            f.write(date.strip()+"\n")
        f.close()
    except TimeoutException:
        print ("Loading took too much time!")
    driver.quit()