import requests as rq
import pandas as pd
from datetime import datetime

import schedule

from headers import Headers_NF
from process import Processing

class Scraper:
    
    def __init__(self) -> None:
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        self.max_page()
        
    def max_page(self): 
        page = 1
        url = f'https://kf.expert/office/prodazha?page={page}&pay_type_ids=1&separ_group_id=c1&currency_alias=rur&prices_key_prefix=sale_from_all&sessionId=123456'
        source = f'/vapi/listing_more_cards?page={page}&pay_type_ids=1&separ_group_id=c1&currency_alias=rur&prices_key_prefix=sale_from_all&sessionId=123456'
        first = Headers_NF().resp(url, source)
        self.max_page = first['cards'][-2]['pagination']['pages'][-1]['value']
        
    def start_request(self):
        office_data = []
        
        for page in range(1, self.max_page + 1):
            url = f'https://kf.expert/office/prodazha?page={page}&pay_type_ids=1&separ_group_id=c1&currency_alias=rur&prices_key_prefix=sale_from_all&sessionId=123456'
            source = f'/vapi/listing_more_cards?page={page}&pay_type_ids=1&separ_group_id=c1&currency_alias=rur&prices_key_prefix=sale_from_all&sessionId=123456'
            data = Headers_NF().resp(url, source)
            
            local = [ 
                   {
                    "Ссылка": f"https://kf.expert{obj['title']['url']}",
                    'Название' : obj['title']['text'],
                    'Тип' : 'Офисы',
                    'Адрес' : ''.join(a['text'] + ', ' for a in obj['address'][1:])[:-2] if \
                            ''.join(a['text'] + ', ' for a in obj['address'][1:])[:-2] != '' else '',
                    'Город' : 'Москва',
                    'longitude' : obj['coords'].split(',')[1] if obj['coords'] != None else '',
                    'latitude' : obj['coords'].split(',')[0] if obj['coords'] != None else '',
                    'price' : "{} {}".format(obj['price']['itemprop'], obj['price']['currency']),
                            #int(obj['price']['begin'].replace('₽', '').replace(' ', '')) if '₽' in obj['price']['begin'] else\
                            #int(obj['price']['begin'].replace('$', '').replace(' ', '')) * 100 if '$' in obj['price']['begin'] else '',
                    'Дата_сбора' : self.date,
                    'Тип сделки' : 'Купить коммерсию',
                    'latitude' : obj['coords'].split(',')[0] if obj['coords'] != None else '' , 
                    'longitude' : obj['coords'].split(',')[1] if obj['coords'] != None else ''
                    }
                for obj in data["cards"] if 'price' in obj
                ]
            
            office_data += local
            print(page, len(local))
            
        return office_data


def main():
    print('Go')
    scraper = Scraper()
    processor = Processing()
    
    data = scraper.start_request()
    new_data = pd.DataFrame(data)
    
    processor.update_data(new_data)
    print('End')
    
if __name__ == "__main__":
   main()
 
#schedule.every().day.at("15:46").do(main)       


#while True:
#    schedule.run_pending()
    
