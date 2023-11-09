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
    
    def __init__(self) -> None:
        self.session = cloudscraper.create_scraper()
        self.LinksCollector = LinksCollector()
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
    
    def getsoup(self, url):
        response = self.session.get(url = url)
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
        for segment in segments:
            last_page = self.max_page(segment)
            
            if last_page == '':
                urls = self.LinksCollector.collect_links(segment)
                for url in urls:
                    new_url = 'https://kf.expert' + url
                    data.append(self.collect_offer(new_url))
                print(f'Для сегмента {segment} и страницы {1} собрано {len(urls)} предложений')

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

        dict_items = {
                  'Тип здания': 'type_building',
                  'Тип сделки': 'type_deal',
                  'Стадия строительства': 'stage_construction',
                  'Общая площадь': 'total_area',
                  'Класс' : 'class',
                  'Лифты' : 'elevator',
                  'Электроснабжение' : 'electricity_on',
                  'Планировка' : 'layout',
                  'В стоимость включено' : 'price_includes',
                  'Электричество' : 'electricity',
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

        dict_values['description'] = description
        dict_values['total_price'] = total_price
        dict_values['price_meter'] = price_meter + price_wrap
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
    processor.update_data(new_data)
    print('End')
    
if __name__ == "__main__":
   main()
   

    
