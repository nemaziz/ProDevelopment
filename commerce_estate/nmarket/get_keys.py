import requests as rq
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from seleniumwire import webdriver

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
#--log-level=3 --headless
            
class Keys_class:
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(options = chrome_options)
    
    def offers_get_key(self):
        """Получить ключ авторизации для сбора данных со страницы"""
        
        auth = None
        while auth == None:
            self.browser.get('https://auth.nmarket.pro/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Decatalog_spa%26redirect_uri%3Dhttps%253A%252F%252Fspb.nmarket.pro%252F%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520email%2520phone%2520role%2520permission%2520ecatalogApi%26state%3D39ded81c8cb74f04a0a4b9848b29f243%26nonce%3D71d6b39f09cc475ba3aea00a287ace3e')
            
            time.sleep(1)
            login  =  self.browser.find_element(By.ID ,  'login-input' )
            login.send_keys('Vladislav-mv@yandex' + Keys.RETURN) #
            time.sleep(1)
            
            password  =  self.browser.find_element(By.ID ,  'mat-input-1' )
            password.send_keys('Yzp81C' + Keys.RETURN) #
            time.sleep(1)
            
            get_url = """https://spb.nmarket.pro/?isSmartLineMode=true"""
            self.browser.get(f'{get_url}')

            time.sleep(3)
            print('as')
            for request in self.browser.requests:
                if 'authorization' in dict(request.headers):
                    auth = request.headers['authorization']
                    break
        return auth


    def pers_get_key(self, offer_id):
        """Получить ключ для авторизации со страницы объявления"""
        
        get_url = f"""https://spb.nmarket.pro/presentation-new/realtyobject/{offer_id}"""
        self.browser.get(f'{get_url}')
        for request in self.browser.requests:
            if 'authorization' in dict(request.headers):
                auth_pers = request.headers['authorization']
                break
        
        return auth_pers
    
    def house_get_key(self, jk_id):
        """Получить ключ для авторизации со страницы ЖК"""
        
        source = f'https://spb.nmarket.pro/search/complex/{jk_id}?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%221%22,%222%22%5D%7D'
        self.browser.get(f'{source}')
        for request in self.browser.requests:
            if 'authorization' in dict(request.headers):
                #print('atr')
                authjk = request.headers['authorization']
                break   
        return authjk
    
    
#print(Keys_class().offers_get_key())
