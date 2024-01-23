import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper

from process_nf import Processing
from links_scraper import LinksCollector

import re
import requests as rq

segments = [
    'https://kf.expert/spb/office/prodazha',
    'https://kf.expert/spb/street-retail/prodazha',
    'https://kf.expert/spb/office/arenda',
    'https://kf.expert/spb/street-retail/arenda'
]

class Scraper:
    def __init__(self) -> None:
        self.session = cloudscraper.create_scraper()
        self.LinksCollector = LinksCollector()
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        self.headers = rq.utils.default_headers()

    
    def getsoup(self, url):
        self.headers.update({'User-Agent': 'My User Agent 1.0',})
        
        response = self.session.get(url = url, headers=self.headers)
        response.raise_for_status()
        text = response.text
        try:
            soup = BeautifulSoup(text, 'lxml')
        except:
            soup = BeautifulSoup(text, 'html.parser')
        
        return soup
        
    def max_page(self, url):
        soup = self.getsoup(url) 
            
        pages = soup.select("div[class = 'pagination pagination--red']")[0].text.strip().split()
        
        return '' if pages == [] else pages[-1]
    
    def start_request(self):
        data = []
        #segments = ['https://kf.expert/spb/office/prodazha']
        for segment in segments:
            last_page = self.max_page(segment)
            
            if last_page == '':
                urls = self.LinksCollector.collect_links(segment)
                for url in urls:
                    new_url = 'https://kf.expert' + url
                    data.append(self.collect_offer(new_url))
                print(f'Для сегмента {segment} и страницы {1} собрано {len(urls)} предложений')

            else:
                print(last_page)
                for page in range(1, int(last_page) + 1):
                    url_segment = segment + f'?&page={page}#listing'
                    urls = self.LinksCollector.collect_links(url_segment)
                    for url in urls:
                        new_url = 'https://kf.expert' + url
                        data.append(self.collect_offer(new_url))
                    print(f'Для сегмента {segment} и страницы {page} собрано {len(urls)} предложений')
        yield data 
    
    
    def collect_offer(self, url): 
        soup = self.getsoup(url)
        initial_items = {
            'id' : soup.select("span[class *= 'detail-jk-header__id']")[0].text.strip(),
            'url' : url,
            'name' : soup.select("h1[class = 'detail-jk__main-title']")[0].text
        }

        self.dict_items = {
                  'Тип здания': 'type_building',
                  'Тип сделки': 'type_deal',
                  'Стадия строительства': 'stage_construction',
                  'Общая площадь': 'total_area',
                  'Класс' : 'class',
                  'Лифты' : 'elevator',
                  'Электроснабжение' : 'electricity_on',
                  'Планировка' : 'layout',
                  'В стоимость включено' : 'price_includes',
                  'Электричество'  : 'electricity',
                  'Площадь в продажу': 'area_sale',
                  'Площадь блока' : 'area_sale2',
                  'Площадь в аренду' : 'area_sale3',
                  'Свободная площадь' : 'free_area',
                  'Количество доступных блоков в аренду' : 'blocks_cnt',
                  'Дополнительные характеристики' : 'addit_char',
                  'Тип аренды' : 'type_rent',
                  'Свободное кол-во рабочих мест' : 'workers_cnt',
                  'Витрины': 'showcases',
                  'Входная группа': 'entry_group',
                  'НДС': 'tax',
                  'Высота потолков': 'height',
                  'Этаж' : 'floor',
                  'Этажность' : 'floors',
                  'Мощность электроэнергии': 'electricity_intensity',
                  'Операционные расходы' : 'expenses',
                  'Парковочный коэффициент' : 'parking_coef',
                  'Шаг колонн' : 'column',
                  'Площадь здания' : 'area_building',
                  'Отделка': 'decoration',
                  'Город': 'city',
                  'Район': 'district',
                  'Метро': 'metro',
                  'Адрес': 'address',
                  'Год строительства' : 'year_construction',
                  'Предложений в продажу' : 'offer_sale_cnt',
                  'Предложений в аренду' : 'offer_rent_cnt',
                  'Эксклюзивный объект' : 'exclusive',
                  'Доход' : 'income'
                  }

        dict_values = {}

        parametrs =  [a.text.strip() for a in soup.select("div[class = 'characteristic__item-title']")] 
        values = [a.text.replace('\xa0', '').strip() for a in soup.select("div[class = 'characteristic__item-text']")]
        
        for old_key, value in zip(parametrs, values):
                if old_key in self.dict_items:
                    key = self.dict_items[old_key]
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
 
        try:
            image = soup.select_one('div[id = "gallery_plan"] img').get('data-src')
        except:
            image = ''
        
        phone = soup.select("a[class = 'detail-jk-preview__phone comagic_phone']")[0].text.strip()
        
        try:
            coords = soup.select("div[data-center]")[0].get('data-center').split(',')
        except:
            print(url)
            coords = ['', '']
            
        if "запросу" in total_price or pd.isna(total_price):
            total_price = pd.NA
            price_meter = pd.NA
        else:
            try:
                total_price = int(total_price)
            except:
                print('total',url, total_price)
                total_price = int(re.findall(r'([\d]+)', str(total_price))[0])
                
            if dict_values['type_deal'] == 'Продажа':
                price_meter = int(re.findall(r'([\d]+)', price_meter)[0])
                
                if price_meter > total_price:
                    total_price, price_meter = price_meter, total_price
                else:
                    print(url, price_meter, total_price)
            else:
                try:
                    price_meter = int(re.findall(r'([\d]+)', str(price_meter))[0])
                    if price_meter > total_price: 
                        total_price, price_meter = price_meter, total_price//12
                except:
                    print('metr', url, price_meter)
                    price_meter = pd.NA
                    total_price = pd.NA
                    

        dict_values['description'] = description
        dict_values['total_price'] = total_price
        dict_values['price_meter'] = price_meter
        dict_values['phone'] = phone
        dict_values['image'] = image
        dict_values['latitude'] = coords[0]
        dict_values['longitude'] = coords[1]
        dict_values['scrape_date']  =  self.date
        
        initial_items.update(dict_values)
        return initial_items


def main():
    print('Go')
    scraper = Scraper()
    processor = Processing()
    
    data = next(scraper.start_request())
 
    new_data = pd.DataFrame(data)
    print(f'Всего собрано {new_data.shape[0]} объявлений')
    processor.update_data(new_data, scraper.dict_items)
    print('End')
    
if __name__ == "__main__":
   main()
   
#scraper = Scraper()
#url = 'https://kf.expert/spb/office/pomeschenie/optima-ol47180'

#d = scraper.collect_offer(url)
#print(d)
