from dataclasses import dataclass
from difflib import SequenceMatcher
from readline import read_init_file

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

def similar(a : str , b : str ):
    return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    results = []
    with open("results.csv" , "r") as res_file:
        res_file.readline()
        for line in res_file:
            match = ResultsData()
            res_words = line.split(", ")
            match.home = res_words[0]
            match.away = res_words[1]
            match.winner = res_words[2]
            match.cover = res_words[3]
            match.total_bet = res_words[4]
            match.total_by = res_words[5]
            match.date = res_words[6]
            results.append(match)
    mf = open("final_file.csv" , "w")
    headers = "Home, Away, Has-Metric Winner, H.M Cover By, Covers Percent, Covers Attempts, Covers More, Covers Def Percent, Covers Def Attempts, Covers Def More, Date\n"
    mf.write(headers)
    cover_data = []
    with open("coversScrape.csv" , "r") as f:
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
                    data.def_more + "\n"
                    )
            mf.write(w_line)
    print("Dunzo")






