from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

absolute_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saveto = os.path.join(os.path.join(absolute_path, "data"), "all_teams.csv")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
]


profile = FirefoxProfile()
random_user_agent = random.choice(user_agents)
profile.set_preference("general.useragent.override", random_user_agent)

firefox_options = Options()
firefox_options.profile = profile

driver = webdriver.Firefox(options=firefox_options)
# driver.maximize_window()

years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
teams = set()

for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    driver.get(url)

    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "modal-close"))
        )
        close_btn.click()
    except:
        pass

    table_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "div_totals_stats"))
    )

    html = table_div.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    tbody = soup.find("tbody")

    for row in tbody.find_all("tr"):
        if row.get("class") and "thead" in row.get("class"):
            continue
        cells = row.find_all(["th", "td"])
        row_data = [cell.get_text(strip=True) for cell in cells]

        try:
            rank = int(row_data[0])
        except:
            rank = 999
        if rank > 50:
            break

        team = row_data[3]
        if team != "":
            teams.add(team)
            
teams.discard("2TM")

rows = []

for team in teams:
    print(f"Getting {team}'s information...", end='')
    url = f"https://www.basketball-reference.com/teams/{team}/"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "meta"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    meta = soup.find("div", id="meta")

    info = {}
    for p in meta.find_all("p"):
        strong = p.find("strong")
        if strong:
            key = strong.text.replace(":", "").strip()
            value = p.text.replace(strong.text, "").strip()
            info[key] = value

    team_name = meta.find("h1").find("span").text.strip()

    rows.append({
        "id":team,
        "Team": team_name,
        "Location": info.get("Location", ""),
        "Seasons": info.get("Seasons", ""),
        "Record": info.get("Record", ""),
        "Playoff Appearances": info.get("Playoff Appearances", ""),
        "Championships": info.get("Championships", "")
    })
    print('Done!')

df = pd.DataFrame(rows)
df.to_csv(saveto, index=False, encoding="utf-8-sig")

driver.quit()


