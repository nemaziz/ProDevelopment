import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from meta_data import *
from process import Processing

# & o:/Nematov/Web_scraping/ProDevelopment/.venv/Scripts/python.exe o:/Nematov/Web_scraping/ProDevelopment/commerce_estate/Avito/scraper.py

service = Service(executable_path="O:/Nematov/Web_scraping/chromedriver.exe")
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-gpu")

base_url = lambda page: 'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&p={}'.format(page)

class Scraper:
    """Класс для парсинга Авито.
    
    Атрибуты:
        session: webdriver из selenium
        pages: номер последней страницы с объявлениями
        
    Методы:
        get_pages: находит номер последней страницы
        get_soup: получает объект bs4
        get_metro, get_description: нахождение информации о метро и описании соответственно
        get_room_attributes: собирает информацию из раздела 'О Помещении'
        get_building_attributes: собирает информацию из раздела "О здании'
        get_picture: собирает ссылку первой картинки в объявлении
        start_scraper: запуск парсера по всем страницам, собирает информацию, используя методов
    """
    
    def __init__(self) -> None:
        self.session =  webdriver.Chrome(service=service, options=options) #browser #cloudscraper.create_scraper()
        self.pages = self.get_pages()
        
    
    def get_pages(self) -> str:
        """Функция для нахождения номера последней страницы с объявлениями.
        
        Возвращает число.
        """
                
        soup = self.get_soup(base_url(1))
        last_page = soup.select("span[class = 'styles-module-text-InivV']")
        return last_page[-1].text
    
    def get_soup(self, link:str) -> BeautifulSoup:
        """Функция для получения объекта BeautifulSoup страницы объявления
        
        Аргументы:
            link (str): Адрес сайта

        Результат:
            объект BeautifulSoup
        """
        
        self.session.get(url = link)
        page_source = self.session.page_source
        try:
            soup = BeautifulSoup(page_source, 'lxml')
        except:
            soup = BeautifulSoup(page_source, 'html.parser')
        return soup
    
    def get_metro(self, soup:BeautifulSoup) -> str: 
        
        icon_metro = soup.select("span[class ^= 'geo-icons']")
        
        if icon_metro:
            metro = soup.select_one("div[data-marker='item-address']").find('span', attrs={ 'class' : None} ).text.strip()
            print(metro)
            # assert metro in metro_spb, metro
            return metro
        return 'Нет метро'
    
    def get_description(self, soup:BeautifulSoup) -> str:
        """Собирает описание из объявления

        Аргумент:
            soup (bs4): объект bs4

        Результаты:
            str: адрес помещения
        """
        
        address = soup.select("div[itemprop = 'description']").text.strip()
        return address
    
    def get_room_build_attributes(self, soup:BeautifulSoup) -> dict:
        """Собираем характеристики из отдела 'О помещении' и 'О здании'

        Аргументы:
            soup (bs4): объект bs4
            
        Результат: 
            dict: словарь с структурой: {признак: значений}
        """
        
        characters = [[b.text.replace('\xa0', '') for b in a.select("li") ] for a in s.select('[data-marker="item-view/item-params"]')]
        characters = sum(characters, [])
        
        result = {a.split(':')[0] : a.split(':')[1]
                  for a in characters}
        
        return result
    
    def get_building_attributes(self, soup:BeautifulSoup) -> dict:
        """Собираем характеристики из отдела 'О здании'

        Args:
            soup (_type_): объект bs4

        Returns:
            dict: словарь с структурой : {признак: значений}
        """
        
        characters = [a.text.replace(u'\xa0', '') for a in soup.select("li[class = 'style-item-params-list-item-aXXql']")]
        print('build', characters)
        result = {a.split(':')[0] : a.split(':')[1]
                  for a in characters}
        
        return result
    
    def get_picture(self, soup:BeautifulSoup) -> str:
        """Собирает ссылку на первую картинку помещения в объявлении

        Аргумент:
            soup (_type_): объект bs4 

        Результат:
            str: возвращает ссылку на картинку
        """
        
        image = soup.select_one('img[class = "desktop-1ky5g7j"]').get('src')
        
        return image
    
    def start_scraper(self) -> None:
        
        data = {'url' : [],
                'name' : [],
                'price' : [],
                'pricem2' : [],
                'address': [],
                'metro': [], 
                'picture': []}
        
        for page in range(1, 2):
            url = base_url(page)
            soup = self.get_soup(url)
            objects = soup.select("div[data-marker='item']")
            
            links =  ['https://www.avito.ru' + a.select_one("a[data-marker='item-title']").get('href') for a in objects]
            
            for link in links[:3]:
                
                soup = self.get_soup(link)

                room_attrs = self.get_room_attributes(soup)
                for key, value in room_attrs.items():
                    if key not in data:
                        data[key] = ['' for i in range(len(data['url']))] + [value]
                    else:
                        data[key] += [value]
                print('1', data)
                build_attrs = self.get_building_attributes(soup)
                
                for key, value in build_attrs.items():
                    if key not in data:
                        data[key] = ['' for i in range(len(data['url']))] + [value]
                    else:
                        data[key] += [value]
                data['url'].append(link)
                print('2', data)
                time.sleep(3)
                
                for key, value in data.items():
                    orig_ln = len(data['url'])
                    for_ln = len(data[key])
                    if for_ln != orig_ln:
                        data[key] += ['' for a in range(orig_ln - for_ln)]
            
            data['name'] += [a.select_one("[itemprop='name']").text for a in objects]
            data['price'] += [a.select_one("meta[itemprop='price']").get('content') for a in objects]
            data['pricem2'] += [a.select("span[class^='price-root'] p")[-1].get_text(strip=True).replace('\xa0', '') for a in objects]
            data['address'] += [a.select_one("div[data-marker='item-address']").select_one('p').text for a in objects]
            data['picture'] += [a.select_one('[data-marker ^= "slider-image/image"]').get('data-marker').replace('slider-image/image-', '') for a in objects]
        
        return data

        
"""какие характеристики нужны
url, square, price_m2, segment, type_build, type_deal, address, district, latitude, tongitude, image, description, 
"""
        
scraper = Scraper()
link = scraper.get_soup('https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/pomeschenie_svobodnogo_naznacheniya_58_m2._2_etazh_s_o_2387511314')

processor = Processing()

data = scraper.start_scraper()

path = fr'O:\Nematov\Web_scraping\ProDevelopment\commerce_estate\Avito\data'
processor.write_data(pd.DataFrame(data), f'{path}\data.xlsx')

# print(scraper.get_room_attributes(link))
# print(scraper.get_building_attributes(link))
# print(scraper.get_metro(link))
