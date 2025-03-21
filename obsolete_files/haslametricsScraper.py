from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_haslametrics():
    driver = webdriver.Chrome()
    driver.get('http://haslametrics.com/')
    delay = 10

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td[id = 'tdData4'][style = 'visibility: visible;']")))
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        top_row_elems = soup.findAll("td", {"class" : "scoreproj1"})
        bottom_row_elems = soup.findAll("td", {"class" : "scoreproj2"})
        f = open("./output_files/haslametricsScrape.txt", "w")
        home_score = ""
        away_score = ""
        home_team = ""
        away_team = ""
        for away, home in zip(top_row_elems, bottom_row_elems):
            if len(home.findAll()) == 0 and "sc" not in home.get("id"):
                break
            if "sc" in home.get("id"):
                away_score = away.text
                home_score = home.text
            else:
                away_team = away.find("a", {"target" : "_blank"}).text
                home_team = home.find("a", {"target": "_blank"}).text
            if away_score:
                f.write(home_team + "\t" + home_score + "\n")
                f.write(away_team + "\t" + away_score + "\n")
                away_score = ""
        f.close()
        driver.quit()
    except TimeoutException:
        print("didnt work")


# def calculate_haslametrics():
#     with open(f"./output_files/bovadaOdds{TODAYS_DATE}.txt") as file:
#         matches = []
#         for line in file:
#             items = line.split(", ")
#             home_team = items[0]
#             home_spread = items[1]
#             away_team = items[2]
#             away_spread = items[3]
#             total = items[4]
#             date = items[5]
#             bovaData = BovadaData(date, home_team, away_team, home_spread, away_spread, total)
#             matches.append(bovaData)
#     with open("./output_files/haslametricsScrape.txt") as file:
#         count = 1
#         while True:
#             home = file.readline()
#             away = file.readline()
#             if not away: break
#             home = home.split("\t")
#             away = away.split("\t")
#             for m in matches:
#                 if home[0] == m.homeTeam or away[0] == m.awayTeam :
#                     m.hasHomeScore = float(home[1].rstrip())
#                     m.hasAwayScore = float(away[1].rstrip())

#     f = open("./output_files/has_bov.csv", "w")
#     f.write("Home Team, Away Team, Team ATS, ATS Amount, Total Bet, Total Cover By, Date\n")
#     for m in matches:
#         m.calculate_cover()
#         f.write(m.homeTeam + "\t" + m.homeSpread + ", " + m.awayTeam + "\t" + m.awaySpread + ", "  +  m.teamCover + ", " + str(m.coverBy) + ", " + m.has_total_bet + ", " + str(m.has_total_by) + ", " + m.date )


# @dataclass
# class match:
#     homeTeam: str = ""
#     awayTeam: str = ""
#     homeSpread: str = ""
#     awaySpread: str = ""
#     hasHomeScore: float = 0
#     hasAwayScore: float = 0
#     total : str = ""
#     date: str = ""
#     teamCover : str = ""
#     coverBy : float = 0
#     has_total_bet : str = ""
#     has_total_by : float = 0.0

#     def calculate_cover(self):
#         if self.hasAwayScore and self.hasHomeScore:
#             h_cover_score = self.hasHomeScore + float(self.homeSpread)
#             a_cover_score = self.hasAwayScore + float(self.awaySpread)
#             predicted_total = self.hasHomeScore + self.hasAwayScore
#             home_cover = h_cover_score - self.hasAwayScore
#             away_cover = a_cover_score - self.hasHomeScore
#             if home_cover > 0 :
#                 self.teamCover = self.homeTeam
#                 self.coverBy = home_cover
#             else:
#                 self.teamCover = self.awayTeam
#                 self.coverBy = away_cover
#             if predicted_total > float(self.total) :
#                 self.has_total_bet = "Over"
#                 self.has_total_by = predicted_total - float(self.total)
#             else :
#                 self.has_total_bet = "Under"
#                 self.has_total_by = float(self.total) - predicted_total
#             print(self)