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

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
]

profile = FirefoxProfile()
random_user_agent = random.choice(user_agents)
profile.set_preference("general.useragent.override", random_user_agent)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)

options = Options()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.profile = profile

driver = webdriver.Firefox(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.set_page_load_timeout(60)

players = set()
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]

for year in years:
    print(year)
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
    sleep(2)

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", table_div)
    sleep(2)

    html = table_div.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find("tbody")

    for row in tbody.find_all("tr"):
        if row.get("class") and "thead" in row.get("class"):
            continue
        try:
            rank = int(row.find("th").text)
        except:
            rank = 999
        if rank > 50:
            break
        a_tag = row.find("a")
        if a_tag:
            full_link = "https://www.basketball-reference.com" + a_tag['href']
            players.add(full_link)
all_players = []
for player in players:
    url = player
    for attempt in range(3):
        try:
            driver.get(url)
            break
        except:
            if attempt == 2:
                driver.quit()
            sleep(5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        more_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "meta_more_button"))
        )
        driver.execute_script("arguments[0].click();", more_btn)
        sleep(3)
    except:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    info_div = soup.find("div", id="info")

    player_data = {}
    player_data["link"] = player
    if info_div:
        name_tag = info_div.find("h1")
        player_data["Name"] = name_tag.get_text(strip=True) if name_tag else None

        full_text = info_div.get_text()

        if "Position:" in full_text:
            position_start = full_text.find("Position:") + len("Position:")
            position_end = full_text.find("▪", position_start)
            if position_end == -1:
                position_end = full_text.find("Shoots:", position_start)
            if position_end == -1:
                position_end = position_start + 50
            player_data["Position"] = full_text[position_start:position_end].strip()

        if "Shoots:" in full_text:
            shoots_start = full_text.find("Shoots:") + len("Shoots:")
            shoots_text = full_text[shoots_start:shoots_start+20].strip()
            if shoots_text.startswith("Right"):
                player_data["Shoots"] = "Right"
            elif shoots_text.startswith("Left"):
                player_data["Shoots"] = "Left"
            else:
                words = shoots_text.split()
                if words:
                    player_data["Shoots"] = words[0]

        if "Team:" in full_text:
            team_start = full_text.find("Team:") + len("Team:")
            team_end = full_text.find("\n", team_start)
            if team_end == -1:
                team_end = team_start + 50
            player_data["Team"] = full_text[team_start:team_end].strip()

        if "Born:" in full_text:
            born_start = full_text.find("Born:") + len("Born:")
            born_end = full_text.find("in", born_start)
            if born_end != -1:
                born_end = full_text.find("\n", born_end)
            if born_end == -1:
                born_end = born_start + 100
            player_data["Born"] = full_text[born_start:born_end].strip()

        if "Experience:" in full_text:
            exp_start = full_text.find("Experience:") + len("Experience:")
            exp_end = full_text.find("\n", exp_start)
            if exp_end == -1:
                exp_end = exp_start + 20
            player_data["Experience"] = full_text[exp_start:exp_end].strip()

        p_tags = info_div.find_all("p")
        for p in p_tags:
            p_text = p.get_text(strip=True)
            if any(char.isdigit() for char in p_text) and ("lb" in p_text or "'" in p_text):
                p_text = p_text.replace(" ", "").replace("(", " (")
                player_data["Height_Weight"] = p_text
                break

        if player_data:  
            all_players.append(player_data)

df = pd.DataFrame(all_players)
df.to_csv("nba_players_stat.csv", index=False, encoding="utf-8")

driver.quit()

print("end:)))))))))")
