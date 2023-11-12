import pandas as pd
from datetime import datetime

from headers import *
from get_keys import Keys_class
from process import Processing

path = """O:\\Nematov\\Web_scraping\\ProDevelopment\\commerce_estate\\nmarket\\data\\Apartments"""
path_sales = '{}\\Sales.xlsx'.format(path)
path_supply = '{}\\Supply.xlsx'.format(path)
path_house =  '{}\\house.xlsx'.format(path)


class Scraper:
    
    def __init__(self) -> None:
        self.date = f'{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
        
    def collect_offers(self):
        flats_v = []
        page = 1
        while True:
            url = f'''https://spb.nmarket.pro/search/apartmentgrid?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%222%22%5D%7D&apartment.page={page}&apartment.sort=%5B%7B%22name%22:%22roomsSort%22,%22sortOrder%22:0%7D,%7B%22name%22:%22houseShortNameString%22,%22sortOrder%22:0%7D,%7B%22name%22:%22negotiatedPrice%22,%22sortOrder%22:1%7D,%7B%22name%22:%22priceTotal%22,%22sortOrder%22:0%7D%5D'''
            source = '''https://spb.nmarket.pro/search/apartmentgriddata?searchString=%7B%22TTypeObjNewBuildId%22%3A%5B%222%22%5D%7D&isSmartLineMode=false'''
            
            data = resp(url, source, page)
            
            if data == []:
                print('Страницы кончились')
                break
            
            local = [
                {
                    "Ссылка": f"https://spb.nmarket.pro/presentation-new/realtyobject/{obj['id']}",
                    "Тип" : f"{obj['type']}",
                    "Планировка" : "" if obj['planPicture'] == None else f"https://img.nmarket.pro/photo/pid/{obj['planPicture']['guid']}/?type=png&v=1&wpsid=8",
                    "Площадь" : f"{obj['sAll']}",
                    "Жилая_площадь" : f"{obj['sLiving']}",
                    "Площадь_кухни" : f"{obj['sKitchen']}",
                    "Отделка" : f"{obj['decorationName']}",
                    "Санузел" : f"{obj['wcName']}",
                    "Балкон" : f"{obj['balconyName']}",
                    "Этаж" : f"{obj['houseFloorName']}",
                    "Колво_этажей" : "" if obj['floors'] == None else obj['floors'] if int(obj['floors']) < 6 else 5 ,
                    "Номер_объекта" : f"{obj['objectNumber']}",
                    "ЖК" : f"{obj['houseShortNameString']}",
                    "ЖК_айди" : f"{obj['houseId']}",
                    "Продавец" : f"{obj['sellerName']}",
                    "Район" : f"{obj['district']}",
                    "Срок сдачи" : f"{obj['dateBuilt']}",
                    "Цена_100" : obj['priceTotal'],
                    "Цена_за_м" : obj['pricePerSqMeter'],
                    "Базовая_цена" : obj['priceBaseTotal'],
                    "Вознаграждение" : obj['displayedAbsoluteSubagentCommissionValue'],
                    'Тип_квартир' : 'Студия' if obj['isStudio'] else f"{obj['rooms']}ккв",
                    'Дата_сбора' : self.date
                }
                for obj in data 
            ]
            #print(page, len(local))
            flats_v += local
            page += 1
            
        return flats_v
    
    def collect_house(self):
        house_nc = []
        page = 1
        while True:
            url = f'''https://spb.nmarket.pro/search/complexesgrid?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%222%22%5D%7D&page={page}'''
            source = '''https://spb.nmarket.pro/search/complexesgriddata?searchString=%7B%22TTypeObjNewBuildId%22%3A%5B%222%22%5D%7D&isSmartLineMode=false'''

            
            data = resp(url, source, page, hs = True)
            
            if data == []:
                print('End data')
                break
            
            local = [
                {
                    "Ссылка": f"https://spb.nmarket.pro/search/complex/{obj['complexId']}",
                    'id' : obj['complexId'],
                    "Имя" : f"{obj['name']}",
                    "Девелопер" : f"{obj['developers'][0]}" if len(obj['developers']) == 1 else f"{obj['developers']}",
                    "Готовность" : f"{obj['deadlinePeriod']}",
                    "Отделка" : f"{obj['decorations'][0]}" if len(obj['decorations']) == 1 else f"{obj['decorations']}",
                    "Вид_платы" : f"{obj['paymentOptions'][0]}" if len(obj['paymentOptions']) == 1 else f"{obj['paymentOptions']}",
                    "Адрес" : f"{obj['address']}",
                    "Картинка" : f"https:{obj['pictureUrl']}",
                    'Метро' : obj['subwayName'],
                    'Время до метро' : obj['subwayReachFrom'],
                }
                for obj in data
            ]
                
            print('house', page, len(local))
            house_nc += local
            page += 1
        
        return house_nc


def main():
    print('Парсинг начался')
    scraper = Scraper()
    processor = Processing()
    
    offers = scraper.collect_offers()
    new_offers = pd.DataFrame(offers)
    new_offers['ЖК'] = new_offers['ЖК'].str.replace(' [\d] оч. .*', '')
    processor.update_data(new_offers, path_sales, path_supply)
    print("Данные объявлений обновлены")
    
    houses = scraper.collect_house()
    new_house = pd.DataFrame(houses)
    processor.update_house(new_house, path_house)
    print('Парсинг закончился')
    
    
if __name__ == "__main__":
    main()