import requests as rq
from datetime import datetime
import pandas as pd

from headers import *
from get_keys import Keys_class

# path = """O:\\Отдел стратегического развития\\Исследовательская работа\\Анализ рынков недвижимости\\Анализ апартаментов\\Статистические данные\\nmarket"""
# path_sales = f'{path}\\Продажи_nmarket.xlsx'
# path_supply = f'{path}\\Предложение_nmarket.xlsx' 
# path_house = f'{path}\\ЖК.xlsx' 


date = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'

class Processing:
    
    def __init__(self) -> None:
        keys_engine = Keys_class()
    
    def write_data(self, data, path):
        data.reset_index(drop=True).to_excel(f'{path}', index = False)
    
    def update_data(self, new_data, path_sales, path_supply):
        try:
            sales = pd.read_excel(path_sales)
            supply = pd.read_excel(path_supply)
        except:
            self.write_data(pd.DataFrame(columns=list(new_data.columns) + ['Дата закрытия']), path_sales)
            self.write_data(pd.DataFrame(columns=new_data.columns), path_supply)
            sales = pd.read_excel(path_sales)
            supply = pd.read_excel(path_supply)
        
        new_supply = new_data[~new_data['Ссылка'].isin(supply['Ссылка'])]
        sold_supply = supply[~supply['Ссылка'].isin(new_data['Ссылка'])]
        remaining_supply = supply[supply['Ссылка'].isin(new_data['Ссылка'])]
        
        print(len(new_supply), len(sold_supply))
        
        if not new_supply.empty:
            aps_data = new_supply['Ссылка'].apply(rom)
            coords = [a['sectionPolygonCoordinates'].replace('[', '').replace(']', '').split(',')[0:2][:2] for a in aps_data ]
            # crds = rom('5585929')['sectionPolygonCoordinates'].replace('[', '').replace(']', '').split(',')[0:2][:2]
            # print(crds)
            new_supply = new_supply.join(
                pd.DataFrame(
                {
                    'Высота потолка': [a['house']['ceilingHeight'] for a in aps_data],
                    'Год_сдачи': [a['house']['yearEnd'] for a in aps_data],
                    'Квартал_сдачи': [a['house']['quarterEnd'] for a in aps_data],
                    'Тип_дома': [a['house']['typeName'] for a in aps_data],
                    'Парковка': [a['house']['parkingName'] for a in aps_data],
                    'Вариант_оплаты': [a['house']['paymentOptionsString'] for a in aps_data],
                    'Договор': [a['house']['contractTypeShortName'] for a in aps_data],
                    'latitude' : [a[0] for a in coords],
                    'longitude' : [a[1] for a in coords]                    
                },
                index=new_supply.index
            ))
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)
        
        if not sold_supply.empty:
            sold_supply['Дата закрытия'] = date
            
            save_sales = pd.concat([sales, sold_supply])
            self.write_data(save_sales, path_sales)
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)        
    
    def update_house(self, new_data, path_house):
        try:
            old_jk = pd.read_excel(path_house)
        except:
            self.write_data(pd.DataFrame(columns=new_data.columns), path_house)
            old_jk = pd.read_excel(path_house)
            
        supp_new = new_data[~new_data['Ссылка'].isin(old_jk['Ссылка'])]
        
        if not supp_new.empty:
            new_data = supp_new['Ссылка'].apply(jk_data)
            
            print(new_data[0]['advantages'])
            supp_new = supp_new.join(
                pd.DataFrame(
                    {
                        'latitude' : [a['mapPoints'][0]['latitude'] if 'mapPoints' in a else '' for a in new_data],
                        'longitude' : [a['mapPoints'][0]['longitude'] if 'mapPoints' in a else '' for a in new_data],
                        'Достоинства' :  [a['advantages'] for a in new_data]
                    },
                    index = supp_new.index
                )
            )  
                    
            new_old_supp = pd.concat([old_jk, supp_new])
            self.write_data(new_old_supp, path_house)
        