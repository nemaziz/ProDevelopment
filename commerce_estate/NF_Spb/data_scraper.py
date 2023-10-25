import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper

from links_scraper import LinksCollector
from process import Processing

segments = [
    'https://kf.expert/spb/office/prodazha',
    'https://kf.expert/spb/street-retail/prodazha',
    'https://kf.expert/spb/office/arenda',
    'https://kf.expert/spb/street-retail/arenda'
]

class Scraper:
    
    def __init__(self, session) -> None:
        self.session = session
        self.LinksCollector = LinksCollector(self.session)
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        
    def max_page(self, url):
        response = self.session.get(url = url)
        response.raise_for_status()
        text = response.text
        try:
            soup = BeautifulSoup(text, 'lxml')
        except:
            soup = BeautifulSoup(text, 'html.parser')
            
        pages = soup.select("div[class = 'pagination pagination--red']")[0].text.strip().split()
        
        return '' if pages == [] else pages[-1]
    
    def start_request(self):
        data = []
        for segment in segments:
            last_page = self.max_page(segment)
            
            if last_page == '':
                urls = self.LinksCollector.collect_links(segment)
                for url in urls:
                    new_url = 'https://kf.expert' + url
                    data.append(self.collect_offer(new_url))
                print(f'Для сегмента {segment} и страницы {1} собрано {len(urls)} объявлений')
            else:
                for page in range(1, int(last_page) + 1):
                    url_segment = segment + f'?&page={page}#listing'
                    urls = self.LinksCollector.collect_links(url_segment)
                    for url in urls:
                        new_url = 'https://kf.expert' + url
                        data.append(self.collect_offer(new_url))   
                    
                    print(f'Для сегмента {segment} и страницы {page} собрано {len(urls)} предложений')
        yield data 
    
    
    def collect_offer(self, url):    
        resp = self.session.get(url = url)
        text = resp.text
        try:
            soup = BeautifulSoup(text, 'lxml')
        except:
            soup = BeautifulSoup(text, 'html.parser')
        
        initial_items = {
            'id' : soup.select("span[class *= 'detail-jk-header__id']")[0].text.strip(),
            'url' : url,
            'name' : soup.select("h1[class = 'detail-jk__main-title']")[0].text
        }

        dict_items = {'Тип здания': 'type_building',
                    'Тип сделки': 'type_deal',
                    'Стадия строительства': 'stage_construction',
                    'Общая площадь': 'total_area',
                    'Площадь в продажу': 'area_sale',
                    'Площадь блока' : 'area_sale2',
                    'Площадь в аренду' : 'area_sale3',
                    'Витрины': 'showcases',
                    'Входная группа': 'entry_group',
                    'НДС': 'tax',
                    'Высота потолков': 'height',
                    'Этаж' : 'floor',
                    'Этажность' : 'floors',
                    'Мощность электроэнергии': 'electricity',
                    'Отделка': 'decoration',
                    'Город': 'city',
                    'Район': 'district',
                    'Метро': 'metro',
                    'Адрес': 'address',
                    'Год строительства' : 'year_construction',
                    'Предложений в продажу' : 'offer_count',
                    'Доход' : 'income'
                    }

        dict_values = {}

        parametrs =  [a.text.strip() for a in soup.select("div[class = 'characteristic__item-title']")] 
        values = [a.text.replace('\xa0', '').strip() for a in soup.select("div[class = 'characteristic__item-text']")]

        for old_key, value in zip(parametrs, values):
                if old_key in dict_items:
                    key = dict_items[old_key]
                    dict_values[key] = value
                else:
                    dict_values[old_key] = value
        
        
        try:
            description = soup.select("span[class = 'description__text']")[0].text.strip()
        except:
            description = ''
        
        total_price = soup.select("div[class = 'detail-jk-preview__price-list active']")[0].text.replace('\xa0', '').strip()
        
        try:
            price_wrap = soup.select("div[class = 'currency-select__wrap']")[0].text.strip()
        except:
            price_wrap = ''

        try:
            price_meter = soup.select("div[class = 'detail-jk-preview__price-meter active']")[0].text.replace('\xa0', '').strip()
        except:
            price_meter = ''
        
        phone = soup.select("a[class = 'detail-jk-preview__phone comagic_phone']")[0].text.strip()

        dict_values['description'] = description
        dict_values['total_price'] = total_price
        dict_values['price_meter'] = price_meter + price_wrap
        dict_values['phone'] = phone
        dict_values['scrape_date']  =  self.date,
        
        initial_items.update(dict_values)
        
        return initial_items


def main():
    print('Go')
    session = cloudscraper.create_scraper()
    scraper = Scraper(session)
    processor = Processing()
    
    data = next(scraper.start_request())

    new_data = pd.DataFrame(data)
    print(f'Всего собрано {new_data.shape[0]} объявлений')
    processor.update_data(new_data)
    print('End')
    
if __name__ == "__main__":
   main()
   

    
