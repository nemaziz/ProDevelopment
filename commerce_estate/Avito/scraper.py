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
# options.add_argument("--headless=new")
# options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-gpu")

base_url = lambda page: 'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&p={}'.format(page)

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
        return last_page[-1].text
    
    def get_soup(self, link):
        """Функция для получения объекта BeautifulSoup страницы объявления
        
        Аргументы:
            @link (str): Адрес объявления

        Результат:
            объект BeautifulSoup
        """
        
        self.session.get(url = link)
        # print(self.session.page_source)
        page_source = self.session.page_source
        try:
            soup = BeautifulSoup(page_source, 'lxml')
        except:
            soup = BeautifulSoup(page_source, 'html.parser')
        return soup
    
    def get_metro(self, soup):
        
        icon_metro = soup.select("span[class = 'geo-icons-uMILt']")
        
        if icon_metro:
            metro = soup.select_one("div[data-marker='item-address']").find('span', attrs={ 'class' : None} )
            return metro.text.strip()
        return 'Нет метро'
            
    def get_description(self, soup):
        """Собирает описание из объявления

        Аргумент:
            soup (bs4): объект bs4

        Результаты:
            str: адрес помещения
        """
        
        address = soup.select("div[itemprop = 'description']").text.strip()
        return address
    
    def get_room_attributes(self, soup):
        """Собираем характеристики из отдела 'О помещении'

        Аргументы:
            soup (bs4): объект bs4
            
        Результат:
            dict: словарь с структурой: {признак: значений}
        """
        
        characters = [a.text.replace(u'\xa0', '') for a in soup.select("li[class = 'params-paramsList__item-appQw']")]
        result = {a.split(':')[0] : a.split(':')[1]
                  for a in characters}
        
        return result
    
    def get_building_attributes(self, soup):
        """Собираем характеристики из отдела 'О здании'

        Args:
            soup (_type_): объект bs4

        Returns:
            dict: словарь с структурой : {признак: значений}
        """
        
        characters = [a.text.replace(u'\xa0', '') for a in soup.select("li[class = 'style-item-params-list-item-aXXql']")]
        result = {a.split(':')[0] : a.split(':')[1]
                  for a in characters}
        
        return result
    
    def get_picture(self, soup) -> SyntaxError:
        """Собирает ссылку на 1 картинку в объявлении

        Аргумент:
            soup (_type_): объект bs4 

        Результат:
            str: возвращает ссылку на картинку
        """
        
        image = soup.select_one('img[class = "desktop-1ky5g7j"]').get('src')
        
        return image
    
    def start_scraper(self) -> None:
        
        
        # url = base_url(1)
        # soup = self.get_soup(url)
        # objects = soup.select("div[data-marker='item']")
        
        
        data = {'url' : [],
                'name' : [],
                'price' : [],
                'pricem2' : [],
                'address': [],
                'metro': []}
        
        for page in range(1, 2):
            url = base_url(page)
            soup = self.get_soup(url)
            objects = soup.select("div[data-marker='item']")
            
            links =  ['https://www.avito.ru' + a.select_one("a[data-marker='item-title']").get('href') for a in objects]
            
            for link in links[:10]:
                data['url'].append(link)
                soup = self.get_soup(link)
                
                room_attrs = self.get_room_attributes(soup)
                print(link, 'roomm', room_attrs)
                for key, value in room_attrs.items():
                    if key not in data:
                        data[key] = ['' for i in range(len(data['url']))] + [value]
                    else:
                        data[key] += value
                
                build_attrs = self.get_building_attributes(soup)
                print(link, 'blds', build_attrs)
                for key, value in build_attrs.items():
                    if key not in data:
                        data[key] = ['' for i in range(len(data['url']))] + [value]
                    else:
                        data[key] += value
                
                time.sleep(3)
            
            data['name'] += [a.select_one("h3[itemprop='name']").text for a in objects]
            data['price'] += [a.select_one("meta[itemprop='price']").get('content') for a in objects]
            data['pricem2'] += [a.select("span[class^='price-root'] p")[-1].get_text(strip=True).replace('\xa0', '') for a in objects]
            data['address'] += [a.select_one("div[data-marker='item-address']").select_one('p').text for a in objects]
            data['metro'] += [self.get_metro(a) for a in objects]
            
        
        return data
        # print(len(links))
        # print(links[0], names[0], price[0], pricem2[0], address[0], metro[0])
        # print(links[-1], names[-1], price[-1], pricem2[-1], address[-1], metro[-1])
        
"""какие характеристики нужны
url, square, price_m2, segment, type_build, type_deal, address, district, latitude, tongitude, image, description, 
"""
        
scraper = Scraper()
link = scraper.get_soup('https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/pomeschenie_svobodnogo_naznacheniya_58_m2._2_etazh_s_o_2387511314')

print(scraper.get_room_attributes(link))
print(scraper.get_building_attributes(link))
print(scraper.get_picture(link))

print(scraper.start_scraper())
