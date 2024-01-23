import requests as rq
from datetime import datetime
import pandas as pd

date = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'

class Processing:
    
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
            new_supply = new_supply.join(
                pd.DataFrame(
                {
                    'Высота потолка': [a['house']['ceilingHeight'] for a in aps_data],
                    'Год_сдачи': [a['house']['yearEnd'] for a in aps_data],
                    'Квартал_сдачи': [a['house']['quarterEnd'] for a in aps_data],
                    'Тип_дома': [a['house']['typeName'] for a in aps_data],
                    'Парковка': [a['house']['parkingName'] for a in aps_data],
                    'Вариант_оплаты': [a['house']['paymentOptionsString'] for a in aps_data],
                    'Договор': [a['house']['contractTypeShortName'] for a in aps_data]
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
            
            supp_new = supp_new.join(
                pd.DataFrame(
                    {
                        'latitude' : [a['mapPoints'][0]['latitude'] for a in new_data],
                        'longitude' : [a['mapPoints'][0]['longitude'] for a in new_data],
                        'Достоинства' :  [ b['advantages'] for b in new_data]
                    },
                    index = supp_new.index
                )
            )
                    
            new_old_supp = pd.concat([old_jk, supp_new])
            self.write_data(new_old_supp, path_house)
        