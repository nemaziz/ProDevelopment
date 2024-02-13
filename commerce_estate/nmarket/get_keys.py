import requests as rq
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from seleniumwire import webdriver

chrome_options = Options()
# options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--log-level=3")
# chrome_options.add_argument("--headless")
#--log-level=3 --headless
            
class Keys_class:
    def __init__(self) -> None:
        pass
    
    def open_browser(self):
        self.browser = webdriver.Chrome(options = chrome_options)
        
    def authentication(self):
        """Авторизация на сайте nmarket
        """
        path = fr'O:\Nematov\Web_scraping\ProDevelopment\commerce_estate\nmarket'

        with open(fr'{path}\passwords.txt', 'r') as f:
            login_pass = f.readline().strip()
            pass_pass = f.readline().strip()
    
        
        self.browser.get('https://auth.nmarket.pro/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Decatalog_spa%26redirect_uri%3Dhttps%253A%252F%252Fspb.nmarket.pro%252F%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520email%2520phone%2520role%2520permission%2520ecatalogApi%26state%3D39ded81c8cb74f04a0a4b9848b29f243%26nonce%3D71d6b39f09cc475ba3aea00a287ace3e')
        time.sleep(1)
        to_click = self.browser.find_element(By.ID ,  'mat-tab-label-0-1' )
        to_click.click()
        
        time.sleep(1)
        login  =  self.browser.find_element(By.ID ,  'login-input' )
        login.send_keys(login_pass + Keys.RETURN)
        time.sleep(1)
        
        password  =  self.browser.find_element(By.ID ,  'mat-input-2' )
        password.send_keys(pass_pass + Keys.RETURN)
        time.sleep(1)
    
    def offers_get_key(self):
        """Получить ключ авторизации для сбора данных со страницы"""
        
        auth = None
        while auth == None:
            self.open_browser()
            self.authentication()
            
            get_url = """https://spb.nmarket.pro/?isSmartLineMode=true"""
            self.browser.get(f'{get_url}')

            time.sleep(3)
            for request in self.browser.requests:
                if 'authorization' in dict(request.headers):
                    print('Ключ для парсинга страниц найден')
                    auth = request.headers['authorization']
                    break
                
        self.close_browser()
        return auth


    def pers_get_key(self, offer_id):
        """Получить ключ для авторизации со страницы объявления"""
        auth_pers = None
        
        self.open_browser()
        self.authentication()
        
        get_url = f"""https://spb.nmarket.pro/presentation-new/realtyobject/{offer_id}"""
        time.sleep(1)
        self.browser.get(f'{get_url}')
        time.sleep(1)
        for request in self.browser.requests:
            if 'authorization' in dict(request.headers):
                auth_pers = request.headers['authorization']
                print('Ключ для парсинга страниц объявлений найден')
                break
        
        self.close_browser()
        return auth_pers
    
    def house_get_key(self, jk_id):
        """Получить ключ для авторизации со страницы ЖК"""
        
        self.open_browser()
        self.authentication()
        
        source = f'https://spb.nmarket.pro/search/complex/{jk_id}?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%221%22,%222%22%5D%7D'
        time.sleep(1)
        self.browser.get(f'{source}')
        time.sleep(1)
        for request in self.browser.requests:
            if 'authorization' in dict(request.headers):
                print('Ключ для парсинга страницы ЖК найден')
                authjk = request.headers['authorization']
                break  
            
        self.close_browser() 
        return authjk
    
    def close_browser(self):
        self.browser.quit()


