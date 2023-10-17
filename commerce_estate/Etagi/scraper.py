import requests as rq
import pandas as pd
from datetime import datetime

from headers import headers_etagi

def process_location(address, house_num):
        tags = {'city' : 'город',
                'district' : 'район',
                'street' : 'улица'}
        
        result = ""
        
        for tag, value in tags.items():
            result += '' if tag not in address else '{} {}, '.format(address[tag], value)
        
        result += '' if not house_num else '{}'.format(house_num)
        
        return result

class Scraper:
    
    def __init__(self) -> None:
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        
    def start_request(self):
         data = []
         
         page = 1
         request = headers_etagi.get_json(1)
         
         while request['data'] != []:
             request = headers_etagi.get_json(page)
             local = [
                 {
                    'id' : obj['object_id'],
                    "url": f"https://spb.etagi.com/realty/{obj['object_id']}",
                    'name' : obj['class'],
                    'type' : obj['type'],
                    'address' : process_location(obj['meta'], obj['house_num']),
                    'city' : 'Санкт Петербург',
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
                 for obj in data["data"]
                ]
             data += local
             page += 1
             
         yield data
             
             
new_data = Scraper().start_request()
print(next(new_data))