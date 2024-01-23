import requests as rq
import pandas as pd
from datetime import datetime

from headers import headers_etagi
from process import processing

def process_location(address, house_num):
        tags = {'city' : 'город',
                'district' : 'район',
                'street' : 'улица'}
        
        result = ""
        
        for tag, value in tags.items():
            result += '' if tag not in address else '{} {}, '.format(address[tag], value)
        
        result += '' if not house_num else '{}'.format(house_num)

        """Если номера дома нет, то надо убирать с конца запятую и пробел.
        Во всех собранных объявлениях был номер дома, но решил написать проверку"""
        return result if result[-2:] == ', ' else result[:-2]


class Scraper:
    
    def __init__(self) -> None:
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        
    def start_request(self):
        data = []
        
        "Меняешь параметр, чтобы собирать данные для аренды и продажи"
        for action in ['sale', 'lease']:
            page = 1
            request = next(headers_etagi.get_json(1, action))

            while request['data'] != []:
                request = next(headers_etagi.get_json(page, action))
                local = [
                     {
                        'id' : obj['object_id'],
                        "url": f"https://spb.etagi.com/commerce/{obj['object_id']}",
                        'name' : obj['class'],
                        'type' : obj['type'],
                        'action_sl' : obj['action_sl'],
                        'address' : process_location(obj['meta'], obj['house_num']),
                        'district' : obj['meta']['district'],
                        'city' : obj['meta']['city'],
                        'latitude' : obj['la'],
                        'longitude' : obj['lo'],
                        'price' : obj['price'],
                        'price_m2' : obj['price_m2'],
                        'square' : obj['square'],
                        'scrape_date' : self.date,
                        'parking' : obj['parking'],
                        'metro_station' : obj['metro_station'],
                        'time_to_metro' : obj['time_to_metro'],
                        'old_price' : obj['old_price'],
                        'floor' : obj['floor'],
                        'floors' : obj['floors'],
                        'location' : obj['location'],
                        'main_photo_ur' : 'https://cdn.esoft.digital/19201080{}'.format(obj['main_photo'])
                    }
                     for obj in request["data"]
                    ]
                data += local
                print(f'Собрана информация с {page} страницы по {action}')
                page += 1
             
        yield data
             
def main():
    print('Go')
    scraper = Scraper()
    processor = processing()
    
    data = next(scraper.start_request())
    new_data = pd.DataFrame(data)
    print(f'Всего собрано {new_data.shape[0]} объявлений')
    print(f'Включены объявления  из городов: {", ".join(new_data["city"].unique())}')
    processor.update_data(new_data)
    
    print('End')
    
if __name__ == "__main__":
   main()