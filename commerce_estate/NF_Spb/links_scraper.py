import requests as rq
from bs4 import BeautifulSoup

class LinksCollector:
    
    def __init__(self,
                 session) -> None:
        self.session  = session
    
    
    def collect_links(self, url):
            response = self.session.get(url = url)
            response.raise_for_status()
            text = response.text
            try:
                soup = BeautifulSoup(text, 'lxml')
            except:
                soup = BeautifulSoup(text, 'html.parser')
                
            tables = soup.select("div[class ='card-table listing__card-table']")
            objs = soup.select("div[class ='card listing__card']")
            urls_tables = [resp.select("a[class = 'card-table__link']")[0].get('href') for resp in tables]
            urls = [resp.select("a[class = 'card__link']")[0].get('href') for resp in objs]            
            for url_table in urls_tables:
                url = 'https://kf.expert' + url_table
                resp = self.session.get(url = url)
                text = resp.text
                try:
                    soup = BeautifulSoup(text, 'lxml')
                except:
                    soup = BeautifulSoup(text, 'html.parser')
                    offers = soup.select("a[class = 'app-filter__sort-content-item']")
                    url_offers = [a.get('href') for a in offers]
                    urls += url_offers
                        
            return urls
    

