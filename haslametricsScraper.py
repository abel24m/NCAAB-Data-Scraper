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


