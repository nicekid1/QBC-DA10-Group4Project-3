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
saveto = os.path.join(os.path.join(absolute_path, "data"), "all_players.csv")

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
alphabet = 'abcdefghijklmnopqrstuvwyz'
players = []
for char in alphabet:
    print(f'Getting Players starting with {char}...', end='')
    url = f'https://www.basketball-reference.com/players/{char}/'
    driver.get(url)

    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "modal-close"))
        )
        close_btn.click()
    except:
        pass

    table_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "div_players"))
    )

    html = table_div.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    tbody = soup.find('tbody')
    for row in tbody.find_all('tr'):
        player = {}
        if row.get('class') and 'thead' in row.get('class'):
            continue
        cells = row.find_all(['th', 'td'])
        for cell in cells:
            value = cell.get_text(strip=True)
            key = cell.get('data-stat')
            player[key] = value
        pid = row.find('a')
        if pid:
            player['id'] = pid['href']
        active = row.find('strong')
        player['is_active'] = True if active else False
        players.append(player)
    print('Done!')
    
all_players = pd.DataFrame(players)
all_players.to_csv(saveto, index=False, encoding='utf-8-sig')

driver.quit()
