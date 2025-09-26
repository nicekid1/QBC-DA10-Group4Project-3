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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
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
            
print(players)