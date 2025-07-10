import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper

from process import Processing
import time

class Scraper:
    
    def __init__(self) -> None:
        self.session = cloudscraper.create_scraper()
        
    def getsoup(self, url): 
        response = self.session.get(url = url)
        response.raise_for_status() 
        text = response.text
        try:
            soup = BeautifulSoup(text, 'lxml')
        except:
            soup = BeautifulSoup(text, 'html.parser')
        
        return soup
    
    def start_request(self):
        data = []
        page = 1

        while True:
            url = f'https://brightrich.ru/sklady/?groupby=product&view=default&page={page}'
            soup = self.getsoup(url)
            
            objects = soup.select("div[class = 'realty-item is-object']")
            if not objects:
                break
            
            urls = [a.select("a[href]")[0].get('href') for a in objects]
            
            for building in urls:
                soup1 = self.getsoup(building)
                offers = soup1.select("a[class = 'commerce-var-mainbox']")#[0].get('href')
                
                try:
                    descr = soup1.select_one('div[data-truncated-text]').text.strip()
                except:
                    descr = ''
                    
                name = soup1.select_one('h1').text
                
                for offer in offers:
                    url = offer.get('href')
                    
                    initial_data = {
                        'Ссылка' : url,
                        'Комплекс' : name,
                        'Описание' : descr
                            }
                    initial_data.update(self.collect_offer(url))
                    data.append(initial_data)
                    
                if not offers:
                    url = building #offer.get('href')

                    initial_data = {
                        'Ссылка' : url,
                        'Комплекс' : name,
                        'Описание' : descr
                    }
                    
                    initial_data.update(self.collect_offer(building))
                    data.append(initial_data)
                    
                time.sleep(3)
                    
            print("На странице {} собрано {} объявлений".format(page, len(urls)))
            page += 1
            
        return data
    
    def collect_offer(self, url):
        offer = self.getsoup(url)

        offer_data = {}
        
        try:
            space = offer.select("div[class = 'commerce-offer-value']")[0].select_one("p[class]")
            assert offer.select("div[class = 'commerce-offer-value']")[0].select('p')[0].text == 'Площадь', 'Проблема с площадью'
            
            space = space.text.replace('\xa0', '').replace('м2', '').strip()
        except:
            space = ''
            
        try:
            price = offer.select("div[class = 'commerce-offer-value']")[1].select_one("span[data-period-group = 'price']")
            meas = offer.select("div[class = 'commerce-offer-value']")[1].select_one('div').text
            assert 'Ставка' in meas or 'Стоимость' in meas, url + ' Проблема с ценой'

            if price == None:
                price = offer.select("div[class = 'commerce-offer-value']")[1].select_one("p[class = 'offer-value']")
                
            price = price.text.replace('\xa0', '').replace('₽/м2', '')
        except:
            price = ''
        
        try:
            deal_type = 'Аренда' if 'Аренда' in offer.select_one("h1").text else 'Продажа' if 'Продажа'\
                in offer.select_one("h1").text else ''
        except:
            deal_type = ''
        
        offer_data['Ставка за м2'] = price
        offer_data['Площадь'] = space
        offer_data['Тип платы'] = deal_type
        
        data = offer.select("p[class = 'product-property-line']")

        
        for i in data :
                key = i.select('span')[0].text
                value = i.select('span')[1].text.replace('\xa0', '').strip()
                offer_data[key] = value

        return offer_data
        


def main():
    print('Go')
    scraper = Scraper()
    processor = Processing()
    
    data = scraper.start_request()

    new_data = pd.DataFrame(data)
    new_data.loc[:, 'Дата_сбора'] =  f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
    print(f'Всего собрано {new_data.shape[0]} объявлений')
    #print(new_data)
    
    processor.update_data(new_data)
    print('End')
    
if __name__ == "__main__":
   main()
   

    
