import string
from dataclasses import dataclass
from difflib import SequenceMatcher

from bovadaWebScraper import scrape_bovada
from coversScraper import scrape_covers
from haslametricsScraper import scrape_haslametrics

@dataclass
class ResultsData:
    home : str = ""
    away : str = ""
    winner : str = ""
    cover : str = ""
    total_bet : str = ""
    total_by : str = ""
    key_stats_p : str = ""
    key_stats_a : str = ""
    more_stats : str = ""
    date : str = ""

@dataclass()
class CoversData:
    home : str = ""
    away : str = ""
    percent : str = ""
    attempts : str = ""
    more : str = ""
    def_percent: str = ""
    def_attempts: str = ""
    def_more: str = ""
    date : str = ""

def similar(a : str , b : str ):
    return SequenceMatcher(None, a, b).ratio()


def build_final_file():
    results = []
    with open("./output_files/has_bov.csv" , "r") as res_file:
        res_file.readline()
        for line in res_file:
            result = ResultsData()
            res_words = line.split(", ")
            result.home = res_words[0]
            result.away = res_words[1]
            result.winner = res_words[2]
            result.cover = res_words[3]
            result.total_bet = res_words[4]
            result.total_by = res_words[5]
            result.date = res_words[6]
            results.append(result)
    mf = open("./output_files/final_results.csv" , "w")
    headers = "Home, Away, Has-Metric Winner, H.M Cover By, Covers Percent, Covers Attempts, Covers More, Covers Def Percent, Covers Def Attempts, Covers Def More, Total Bet (Has), Total By (Has), Date\n"
    mf.write(headers)
    cover_data = []
    with open("./output_files/coversScrape.csv" , "r") as f:
        for line in f:
            data = CoversData()
            data_split = line.split(", ")
            data.home = data_split[0]
            data.away = data_split[1]
            data.percent = data_split[2]
            data.attempts = data_split[3]
            data.more = data_split[4]
            data.def_percent = data_split[5]
            data.def_attempts = data_split[6]
            data.def_more = data_split[7]
            data.date = data_split[8]
            found_match = False
            for r in results:
                r_home = r.home.split("\t")[0]
                r_away = r.away.split("\t")[0]
                if data.home.lower() == r_home.lower() or data.away.lower() == r_away.lower():
                    w_line = (
                        r.home + ", " +
                        r.away + ", " +
                        r.winner + ", " +
                        r.cover + ", " +
                        data.percent + ", " +
                        data.attempts + ", " +
                        data.more + ", " +
                        data.def_percent + ", " +
                        data.def_attempts + ", " +
                        data.def_more + ", " +
                        r.total_bet + ", " +
                        r.total_by + ", " +
                        r.date
                              )
                    print(w_line)
                    mf.write(w_line)
                    results.remove(r)
                    found_match = True
            if not found_match:
                cover_data.append(data)
    if len(cover_data) > 0:
        for r in results:
            w_line = (
                    r.home + ", " +
                    r.away + ", " +
                    r.winner + ", " +
                    r.cover + ", " +
                    ", " +
                    ", " +
                    ", " +
                    ", " +
                    ", " +
                    ", " +
                    ", " +
                    ", " +
                    r.date
            )
            mf.write(w_line)
            results.remove(r)
        for data in cover_data:
            w_line = (
                    data.home + ", " +
                    data.away + ", " +
                     ", " +
                     ", " +
                    data.percent + ", " +
                    data.attempts + ", " +
                    data.more + ", " +
                    data.def_percent + ", " +
                    data.def_attempts + ", " +
                    data.def_more + ", " +
                    ", " +
                    ", " +
                    data.date + "\n"
                    )
            mf.write(w_line)
    print("Dunzo")

@dataclass
class match:
    homeTeam: str = ""
    awayTeam: str = ""
    homeSpread: str = ""
    awaySpread: str = ""
    hasHomeScore: float = 0
    hasAwayScore: float = 0
    total : str = ""
    date: str = ""
    teamCover : str = ""
    coverBy : float = 0
    has_total_bet : str = ""
    has_total_by : float = 0.0

    def calculate_cover(self):
        if self.hasAwayScore and self.hasHomeScore:
            h_cover_score = self.hasHomeScore + float(self.homeSpread)
            a_cover_score = self.hasAwayScore + float(self.awaySpread)
            predicted_total = self.hasHomeScore + self.hasAwayScore
            home_cover = h_cover_score - self.hasAwayScore
            away_cover = a_cover_score - self.hasHomeScore
            if home_cover > 0 :
                self.teamCover = self.homeTeam
                self.coverBy = home_cover
            else:
                self.teamCover = self.awayTeam
                self.coverBy = away_cover
            if predicted_total > float(self.total) :
                self.has_total_bet = "Over"
                self.has_total_by = predicted_total - float(self.total)
            else :
                self.has_total_bet = "Under"
                self.has_total_by = float(self.total) - predicted_total
            print(self)

def calculate_haslametrics():
    with open("./output_files/bovadaOdds.txt") as file:
        count = 1
        matches = []
        m = match()
        for line in file:
            items = line.split("\t")
            match count:
                case 1:
                    m.awayTeam= items[0]
                    m.awaySpread = items[1]
                case 2:
                    m.homeTeam = items[0]
                    m.homeSpread = items[1]
                case 3:
                    m.total = items[0].strip()
                case 4:
                    m.date = items[0]
            if count == 4:
                matches.append(m)
                m = match()
                count = 1
            else :
                count += 1

    with open("./output_files/haslametricsScrape.txt") as file:
        count = 1
        while True:
            home = file.readline()
            away = file.readline()
            if not away: break
            home = home.split("\t")
            away = away.split("\t")
            for m in matches:
                if home[0] == m.homeTeam or away[0] == m.awayTeam :
                    m.hasHomeScore = float(home[1].rstrip())
                    m.hasAwayScore = float(away[1].rstrip())

    f = open("./output_files/has_bov.csv", "w")
    f.write("Home Team, Away Team, Team ATS, ATS Amount, Total Bet, Total Cover By, Date\n")
    for m in matches:
        m.calculate_cover()
        f.write(m.homeTeam + "\t" + m.homeSpread + ", " + m.awayTeam + "\t" + m.awaySpread + ", "  +  m.teamCover + ", " + str(m.coverBy) + ", " + m.has_total_bet + ", " + str(m.has_total_by) + ", " + m.date )
    f.close()

if __name__ == '__main__':
    # scrape_bovada()
    # scrape_haslametrics()
    # scrape_covers()
    #
    # calculate_haslametrics()
    build_final_file()



