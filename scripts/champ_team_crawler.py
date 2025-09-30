import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import os
warnings.filterwarnings("ignore")

absolute_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saveto = os.path.join(os.path.join(absolute_path, "data"), "nba_champs.csv")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
]

profile = FirefoxProfile()
profile.set_preference("general.useragent.override", random.choice(user_agents))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)

options = Options()
options.headless = False
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.profile = profile

driver = webdriver.Firefox(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.set_page_load_timeout(60)

years = [2019,2020,2021,2022,2023,2024,2025]
champ_team_link = []
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    for attempt in range(3):
        try:
            driver.get(url)
            break
        except:
            if attempt == 2:
                driver.quit()
            sleep(5)

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

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", table_div)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    info_div = soup.find("div", id="info")
    champ_strong = info_div.find("strong", string="League Champion")
    champion_link = champ_strong.find_next("a")["href"]
    link = "https://www.basketball-reference.com"+champion_link
    champ_team_link.append(link)

dfs = pd.DataFrame()
for link in champ_team_link:
    driver.get(link)
    team_id = link.split("/")[4]
    year = link.split("/")[5].replace(".html", "")
    print(f'Getting champion of {year}...', end='')
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "modal-close"))
        )
        close_btn.click()
    except:
        pass

    table_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "div_roster"))
    )

    html = table_div.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    columns = [th.get_text(strip=True) for th in soup.find("thead").find_all("th")]
    columns.append("player_link")
    columns.append('team_id')
    columns.append('year')
    tbody = soup.find("tbody")
    data = []
    for row in tbody.find_all("tr"):
        if row.get("class") and "thead" in row.get("class"):
            continue
        cells = row.find_all(["th", "td"])
        row_data = [cell.get_text(strip=True) for cell in cells]

        player_cell = row.find("td", {"data-stat": "player"})
        player_link = None
        if player_cell:
            a_tag = player_cell.find("a")
            if a_tag:
                player_link = "https://www.basketball-reference.com" + a_tag["href"]
        row_data.append(player_link)
        row_data.append(team_id)
        row_data.append(year)
        data.append(row_data)
    
    df = pd.DataFrame(data, columns=columns)
    dfs = pd.concat([df, dfs], ignore_index=True)
    print('Done!')

dfs.to_csv(saveto, index=False, encoding="utf-8-sig")
driver.quit()