import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# & o:/Nematov/Web_scraping/ProDevelopment/.venv/Scripts/python.exe o:/Nematov/Web_scraping/ProDevelopment/commerce_estate/Avito/scraper.py

service = Service(executable_path="O:/Nematov/Web_scraping/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-gpu")
browser = webdriver.Chrome(service=service, options=options)


base_url = lambda page: 'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/' + \
           'prodam-ASgBAgICAUSwCNJW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&p={}'.format(page)
           
class Scraper:
    """Класс для парсинга Авито.
    
    Атрибуты:
        session: webdriver из selenium
        pages: последняя страница
        
    Методы:
        get_pages: находит номер последней страницы
        get_soup: получает объект bs4
    """
    
    def __init__(self) -> None:
        self.session =  webdriver.Chrome(service=service, options=options) #browser #cloudscraper.create_scraper()
        self.pages = self.get_pages()
    
    
    def get_pages(self) -> None:
        """Функция для нахождения последней страницы.
        
        Присваивает атрибуту pages номер последней страницы.
        """
                
        soup = self.get_soup(base_url(1))
        last_page = soup.select("span[class = 'styles-module-text-InivV']")
        self.pages = last_page[-1].text
    
    def get_soup(self, link):
        """Функция для получения объекта BeautifulSoup страницы объявления
        
        Аргументы:
            @link (str): Адрес объявления

        Результат:
            объект BeautifulSoup
        """
        
        self.session.get(url = link)
        print(self.session.page_source)
        page_source = self.session.page_source
        try:
            soup = BeautifulSoup(page_source, 'lxml')
        except:
            soup = BeautifulSoup(page_source, 'html.parser')
        return soup
    
    def start_scraper(self):
        url = base_url(1)
        
    
        
        
scraper = Scraper()
print(scraper.pages)