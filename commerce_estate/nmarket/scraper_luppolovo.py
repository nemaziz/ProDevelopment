import pandas as pd
from datetime import datetime

from headers import *
from process import Processing

# path = """O:\\Отдел стратегического развития\\Проектная работа\\Проекты ИЖС\\Проект ТНХ Лупполово 1 га\\Статистичекие данные\\Данные по nmarket"""
# gpath_supp = f'{path}\\Предложение_'
# gpath_supp_sell = f'{path}\\Продажи_'

path = """O:\\Nematov\\Web_scraping\\ProDevelopment\\commerce_estate\\nmarket\\data\\Luppolovo"""
path_sales = '{}\\Sales.xlsx'.format(path)
path_supply = '{}\\Supply.xlsx'.format(path)
path_house = '{}\\ЖК.xlsx'.format(path)


class Scraper:
    def __init__(self) -> None:
        self.date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
        
    def collect_offers(self):
        flats_v = []
        page = 1
        while True:
            url = f'''https://spb.nmarket.pro/search/apartmentgrid?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%221%22,%222%22%5D,%22FloorNum%22:%5B%7B%22min%22:null,%22max%22:6%7D%5D%7D&apartment.sort=%5B%7B%22name%22:%22roomsSort%22,%22sortOrder%22:0%7D,%7B%22name%22:%22houseShortNameString%22,%22sortOrder%22:0%7D,%7B%22name%22:%22negotiatedPrice%22,%22sortOrder%22:1%7D,%7B%22name%22:%22priceTotal%22,%22sortOrder%22:0%7D%5D&apartment.page={page}'''
            source = 'https://spb.nmarket.pro/search/apartmentgriddata?searchString=%7B%22TTypeObjNewBuildId%22%3A%5B%221%22%2C%222%22%5D%2C%22FloorNum%22%3A%5B%7B%22min%22%3Anull%2C%22max%22%3A3%7D%5D%7D&isSmartLineMode=false'

            data = resp(url, source, page)
            if data == []:
                print('stop')
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
                for obj in data if (type(obj['floors']) == int and obj['floors'] < 6) or (int(obj['houseFloorName']) < 6)
            ]
            print(f'На странице {page} собраны {len(local)} объявлений')
            flats_v += local
            page += 1
            
        return flats_v


def main():
    print('Go')
    scraper = Scraper()
    processor = Processing()
    
    offers = scraper.collect_offers()
    new_offers = pd.DataFrame(offers)
    new_offers['ЖК'] = new_offers['ЖК'].str.replace(' [\d] оч. .*', '', regex = True)
    
    houses = pd.read_excel(path_house)
    new_offers = new_offers.loc[new_offers['ЖК'].isin(houses['Имя'])].reset_index(drop = True)
    print('update')
    processor.update_data(new_offers,
                          path_sales,
                          path_supply)
    print('End')
    
    
if __name__ == "__main__":
    main()