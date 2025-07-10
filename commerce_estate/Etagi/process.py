import pandas as pd
from datetime import datetime

path = """O:\\Nematov\\Web_scraping\\ProDevelopment\\commerce_estate\\Etagi"""

path_sales = '{}\\data\\Sales.xlsx'.format(path)
path_supply = '{}\\data\\Supply.xlsx'.format(path)
date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'

class processing:
    def write_data(self, data, path):
        data.reset_index(drop=True).to_excel(f'{path}', index = False)
    
    def update_data(self, new_data):
        try:
            sales = pd.read_excel(path_sales)
            supply = pd.read_excel(path_supply)
        except:
            self.write_data(pd.DataFrame(columns=list(new_data.columns) + ['sale_date']), path_sales)
            self.write_data(pd.DataFrame(columns=new_data.columns), path_supply)
            sales = pd.read_excel(path_sales)
            supply = pd.read_excel(path_supply)
        
        new_supply = new_data[~new_data['url'].isin(supply['url'])]
        sold_supply = supply[~supply['url'].isin(new_data['url'])]
        remaining_supply = supply[supply['url'].isin(new_data['url'])]
            
        if not new_supply.empty:
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)
        
        if not sold_supply.empty:
            sold_supply.loc[:, 'sale_date'] = date
            
            save_sales = pd.concat([sales, sold_supply])
            self.write_data(save_sales, path_sales)
            
            save_supply = pd.concat([remaining_supply, new_supply])
            self.write_data(save_supply, path_supply)