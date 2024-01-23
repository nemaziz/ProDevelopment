import pandas as pd
from datetime import datetime 

from yandex_geocoder import Client

#2d6ca6c8-fe89-4f02-bbfa-9b9b0e7a15c5
#d11d3d37-6fc4-4ebd-8ad9-0536bcfc9dd5\
#b22505e2-aedd-48ee-bce9-993aea300a6b
#cf623b28-41e0-4875-835b-c6b808416bab

id_user = "b22505e2-aedd-48ee-bce9-993aea300a6b"
client = Client(id_user)
RADIUS = 500

path = """O:\\Nematov\\Web_scraping\\ProDevelopment\\commerce_estate\\brightrich"""

path_sales = '{}\\data\\Sales.xlsx'.format(path)
path_supply = '{}\\data\\Supply.xlsx'.format(path)

date = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'

class Processing:
    
    def __init__(self) -> None:
        pass
    
    def write_data(self, data, path):
        data.drop_duplicates().reset_index(drop=True).to_excel(f'{path}', index = False)
    
    def update_data(self, new_data):
        try:
            sales = pd.read_excel(path_sales).drop_duplicates(["Ссылка"], keep='first')
            supply = pd.read_excel(path_supply).drop_duplicates(["Ссылка"], keep='first')
        except:
            self.write_data(pd.DataFrame(columns=list(new_data.columns) + ['Дата закрытия']), path_sales)
            self.write_data(pd.DataFrame(columns=new_data.columns), path_supply)
            sales = pd.read_excel(path_sales)
            supply = pd.read_excel(path_supply)
        
        new_supply = new_data[~new_data['Ссылка'].isin(supply['Ссылка'])]
        sold_supply = supply[~supply['Ссылка'].isin(new_data['Ссылка'])]
        remaining_supply = supply[supply['Ссылка'].isin(new_data['Ссылка'])]
            
        if not new_supply.empty:
            new_supply['latitude'] = new_supply['Адрес'].apply(lambda x: float(client.coordinates(x)[0]))
            new_supply['longitude'] = new_supply['Адрес'].apply(lambda x: float(client.coordinates(x)[1]))
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)
        
        if not sold_supply.empty:
            sold_supply['Дата закрытия'] = date
            
            save_sales = pd.concat([sales, sold_supply])
            self.write_data(save_sales, path_sales)
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)
        
        print(f'Продано {len(sold_supply)}\nНовых складов {len(new_supply)}')
            