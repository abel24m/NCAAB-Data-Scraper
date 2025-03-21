import datetime
from dataclasses import dataclass, fields
from difflib import SequenceMatcher
from pathlib import Path

from src.bovadaWebScraper import BovadaWebScraper
from src.coversWebScraper import CoversWebScraper
from obsolete_files.haslametricsScraper import scrape_haslametrics
from src.data.bovadaData import BovadaData


TODAYS_DATE = todays_date = datetime.datetime.now().strftime("%m-%d-%Y")

covers_match_data = []
bov_match_data = []

@dataclass()
class CoversData:
    home: str = ""
    away: str = ""
    percent: float = ""
    more: float = ""
    def_percent: float = ""
    def_more: float = ""
    total_fields_won: int = 0
    average_diff_fields: float = 0.0
    total_data_fields= 4.0
    home_pd : float = 0.0
    away_pd : float = 0.0
    total_opps : int = 0
    date : str = ""


def calculate_covers_winner (data : CoversData):
    home_counter = 0
    away_counter = 0
    home_total = 0
    away_total = 0
    for field in fields(CoversData):
        if field.type is float and  field.name != "average_diff_fields" and field.name != "home_pd" and field.name != "away_pd":
            if float(getattr(data, field.name)) > 0:
                home_counter += 1
                home_total += getattr(data, field.name)
            else:
                away_counter += 1
                away_total += abs(getattr(data, field.name))
    winner = 0
    if home_total > away_total:
        data.total_fields_won = home_counter
        winner = 1
    else:
        data.total_fields_won = away_counter * -1
        winner = -1
    average_diff = (abs(home_total - away_total) / data.total_data_fields) * winner
    data.average_diff_fields = average_diff

def read_covers_data():
    todays_file = Path(f"./output_files/coversScrape{TODAYS_DATE}.csv")
    if not todays_file.is_file():
            print("No Covers File exist for Today : Attempting to Read")
            return
    with open(f"./output_files/coversScrape{TODAYS_DATE}.csv" , "r") as f:
        for line in f:
            data = CoversData()
            data_split = line.split(", ")
            data.home = data_split[0]
            data.away = data_split[1]
            data.home_pd = round(float(data_split[2]), 2)
            data.away_pd = round(float(data_split[3]), 2)
            data.total_opps = int(data_split[4])
            data.percent = round(float(data_split[5]), 2)
            data.more = round(float(data_split[6]), 2)
            data.def_percent = round(float(data_split[7]), 2)
            data.def_more = round(float(data_split[8]), 2)
            data.date = data_split[9]
            calculate_covers_winner(data)

def build_final_file_nba():
    results = []
    with open(f"./output_files/bovadaScrape-NBA-{TODAYS_DATE}.csv" , "r") as bov_file:
        for line in bov_file:
            items = line.split(", ")
            home_team = items[0]
            home_spread = items[1]
            away_team = items[2]
            away_spread = items[3]
            total = items[4]
            date = items[5]
            bovaData = BovadaData(date, home_team, away_team, home_spread, away_spread, total)
            results.append(bovaData)
    mf = open(f"./output_files/final_results-NBA-{TODAYS_DATE}.csv" , "w")
    headers = "Home, Away, Num Fields Won, Avg Diff, Home Point Diff, Away Point Diff, Total Common Opps, Covers Percent, Covers More, Covers Def Percent, Covers Def More, Date\n"
    mf.write(headers)
    cover_data = []
    with open(f"./output_files/coversScrape-NBA-{TODAYS_DATE}.csv" , "r") as f:
        for line in f:
            data = CoversData()
            data_split = line.split(", ")
            data.home = data_split[0]
            data.away = data_split[1]
            data.home_pd = round(float(data_split[2]), 2)
            data.away_pd = round(float(data_split[3]), 2)
            data.total_opps = int(data_split[4])
            data.percent = round(float(data_split[5]), 2)
            data.more = round(float(data_split[6]), 2)
            data.def_percent = round(float(data_split[7]), 2)
            data.def_more = round(float(data_split[8]), 2)
            data.date = data_split[9]
            calculate_covers_winner(data)
            found_match = False
            r : BovadaData
            for r  in results:
                if data.home.lower() == r.home_team.lower() or data.away.lower() == r.away_team.lower():
                    w_line = (
                        r.home_team + "\t " + r.home_spread + "," + #col 1
                        r.away_team + "\t" + r.away_spread + ", " + #col 2
                        str(data.total_fields_won) + ", " + #col 3
                        str(round(data.average_diff_fields,2)) + ", " + #col 4
                        str(data.home_pd)  + ", " +
                        str(data.away_pd)  + ", " +
                        str(data.total_opps)  + ", " +
                        str(data.percent) + ", " + #col 5
                        str(data.more) + ", " + #col 7
                        str(data.def_percent) + ", " + #col 8
                        str(data.def_more) + ", " + #col 10
                        r.date #col 13
                              )
                    mf.write(w_line)
                    results.remove(r)
                    found_match = True
            if not found_match:
                cover_data.append(data)
    if len(cover_data) > 0:
        for r in results:
            w_line = (
                    r.home_team + "\t " + r.home_spread + "," + #col 1
                    r.away_team + "\t" + r.away_spread + ", " + #col 2
                    ", " +
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
        for data in cover_data:
            w_line = (
                    data.home + ", " +
                    data.away + ", " +
                    str(data.total_fields_won) + ", " +
                    str(data.average_diff_fields) + ", " +
                    str(data.home_pd)+ ", " +
                    str(data.away_pd) + ", " +
                    str(data.total_opps) + ", " +
                    str(data.percent) + ", " +
                    str(data.more) + ", " +
                    str(data.def_percent) + ", " +
                    str(data.def_more) + ", " +
                    data.date + "\n"
                    )
            mf.write(w_line)
    mf.close()


def build_final_file_ncaab():
    results = []
    with open(f"./output_files/bovadaScrape-NCAAB-{TODAYS_DATE}.csv" , "r") as bov_file:
        for line in bov_file:
            items = line.split(", ")
            home_team = items[0]
            home_spread = items[1]
            away_team = items[2]
            away_spread = items[3]
            total = items[4]
            date = items[5]
            bovaData = BovadaData(date, home_team, away_team, home_spread, away_spread, total)
            results.append(bovaData)
    mf = open(f"./output_files/final_results-NCAAB-{TODAYS_DATE}.csv" , "w")
    headers = "Home, Away, Num Fields Won, Avg Diff, Home Point Diff, Away Point Diff, Total Common Opps, Covers Percent, Covers More, Covers Def Percent, Covers Def More, Date\n"
    mf.write(headers)
    cover_data = []
    with open(f"./output_files/coversScrape-NCAAB-{TODAYS_DATE}.csv" , "r") as f:
        for line in f:
            data = CoversData()
            data_split = line.split(", ")
            data.home = data_split[0]
            data.away = data_split[1]
            data.home_pd = round(float(data_split[2]), 2)
            data.away_pd = round(float(data_split[3]), 2)
            data.total_opps = int(data_split[4])
            data.percent = round(float(data_split[5]), 2)
            data.more = round(float(data_split[6]), 2)
            data.def_percent = round(float(data_split[7]), 2)
            data.def_more = round(float(data_split[8]), 2)
            data.date = data_split[9]
            calculate_covers_winner(data)
            found_match = False
            r : BovadaData
            for r  in results:
                if data.home.lower() == r.home_team.lower() or data.away.lower() == r.away_team.lower():
                    w_line = (
                        r.home_team + "\t " + r.home_spread + "," + #col 1
                        r.away_team + "\t" + r.away_spread + ", " + #col 2
                        str(data.total_fields_won) + ", " + #col 3
                        str(round(data.average_diff_fields,2)) + ", " + #col 4
                        str(data.home_pd)  + ", " +
                        str(data.away_pd)  + ", " +
                        str(data.total_opps)  + ", " +
                        str(data.percent) + ", " + #col 5
                        str(data.more) + ", " + #col 7
                        str(data.def_percent) + ", " + #col 8
                        str(data.def_more) + ", " + #col 10
                        r.date #col 13
                              )
                    mf.write(w_line)
                    results.remove(r)
                    found_match = True
            if not found_match:
                cover_data.append(data)
    if len(cover_data) > 0:
        for r in results:
            w_line = (
                    r.home_team + "\t " + r.home_spread + "," + #col 1
                    r.away_team + "\t" + r.away_spread + ", " + #col 2
                    ", " +
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
        for data in cover_data:
            w_line = (
                    data.home + ", " +
                    data.away + ", " +
                    str(data.total_fields_won) + ", " +
                    str(data.average_diff_fields) + ", " +
                    str(data.home_pd)+ ", " +
                    str(data.away_pd) + ", " +
                    str(data.total_opps) + ", " +
                    str(data.percent) + ", " +
                    str(data.more) + ", " +
                    str(data.def_percent) + ", " +
                    str(data.def_more) + ", " +
                    data.date + "\n"
                    )
            mf.write(w_line)
    mf.close()



if __name__ == '__main__':
    leagues_to_scrape = ["NCAAB", "NBA"]
    bovscraper = BovadaWebScraper(leagues_to_scrape)
    covscraper = CoversWebScraper(leagues_to_scrape)

    # read_covers_data()
    # read_bovada_data()



    build_final_file_ncaab()
    build_final_file_nba()



