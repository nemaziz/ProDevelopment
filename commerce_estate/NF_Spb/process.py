import pandas as pd
from datetime import datetime 

from yandex_geocoder import Client

id_user = "b22505e2-aedd-48ee-bce9-993aea300a6b"
client = Client(id_user)
RADIUS = 500

path = """O:\\Nematov\\Web_scraping\\ProDevelopment\\commerce_estate\\NF_Spb"""

path_sales = '{}\\data\\Sales.xlsx'.format(path)
path_supply = '{}\\data\\Supply.xlsx'.format(path)

date = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'

class Processing:
    
    def __init__(self) -> None:
        pass
    
    def write_data(self, data, path):
        data.reset_index(drop=True).to_excel(f'{path}', index = False)
    
    def update_data(self, new_data):
        try:
            sales = pd.read_excel(path_sales)
        except:
            self.write_data(pd.DataFrame(columns=list(new_data.columns) + ['Дата закрытия']), path_sales)
            sales = pd.read_excel(path_sales)
        
        try:
            supply = pd.read_excel(path_supply)
        except:
            self.write_data(pd.DataFrame(columns=new_data.columns), path_supply)
            supply = pd.read_excel(path_supply)
        
        new_supply = new_data[~new_data['url'].isin(supply['url'])]
        sold_supply = supply[~supply['url'].isin(new_data['url'])]
        remaining_supply = supply[supply['url'].isin(new_data['url'])]
            
        if not new_supply.empty:
            coords = []
            for address in list(new_supply['address']):
                try:
                    coords.append(float(client.coordinates(address)))
                except:
                    coords.append(['', ''])
                                               
            new_supply.loc[:, ('latitude')] = [a[0] for a in coords]
            new_supply.loc[:, ('longitude')] = [a[1] for a in coords]
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)
        
        if not sold_supply.empty:
            sold_supply.loc[:, ('Дата закрытия')] = date
            
            save_sales = pd.concat([sales, sold_supply])
            self.write_data(save_sales, path_sales)
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)

