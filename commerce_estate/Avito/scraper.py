import pandas as pd
import requests as rq
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

service = Service(executable_path="O:/Nematov/Web_scraping/chromedriver.exe")
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-gpu")
browser = webdriver.Chrome(service=service, options=options)

browser.get('https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&p=2')
soup = BeautifulSoup(browser.page_source, 'lxml')
links = ['https://www.avito.ru' + a.get('href') for a in soup.find_all('a', {'data-marker':'item-title'})]
print(links)

# & o:/Nematov/Web_scraping/ProDevelopment/.venv/Scripts/python.exe o:/Nematov/Web_scraping/ProDevelopment/commerce_estate/Avito/scraper.py