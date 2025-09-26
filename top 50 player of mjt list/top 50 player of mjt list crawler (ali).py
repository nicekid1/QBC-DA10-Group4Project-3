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
print(random_user_agent)
profile.set_preference("general.useragent.override", random_user_agent)

firefox_options = Options()
firefox_options.profile = profile

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()

years = [2019,2020,2021,2022,2023,2024,2025]

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

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", table_div)

    html = table_div.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    columns = [th.get_text(strip=True) for th in soup.find("thead").find_all("th")]
    tbody = soup.find("tbody")
    data = []

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
        data.append(row_data)

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"nba_top50_players_{year}.csv", index=False, encoding="utf-8-sig")
    print(f"nba_top50_players_{year}.csv")
print("the end")
driver.quit()

