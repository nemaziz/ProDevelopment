import requests as rq
from bs4 import BeautifulSoup
import cloudscraper

class LinksCollector:
    
    def __init__(self) -> None:
        self.session  = cloudscraper.create_scraper()
    
    def getsoup(self, url):
        response = self.session.get(url = url)
        response.raise_for_status()
        text = response.text
        try:
            soup = BeautifulSoup(text, 'lxml')
        except:
            soup = BeautifulSoup(text, 'html.parser')
        
        return soup
    
    def collect_links(self, url):
        headers = rq.utils.default_headers()
        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )
    
        response = self.session.get(url = url, headers=headers)
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
        print(len(urls), len(urls_tables))         
        for url_table in urls_tables:    
            url = 'https://kf.expert' + url_table
            soup = self.getsoup(url) 

            pages = soup.select_one('div[class = "pagination__links"]')#.select('a')

            if pages != None and len(pages.select('a')) > 1:
                for i in range(1, len(pages.select('a')) + 1):
                    url = 'https://kf.expert' + url_table.split('?')[0] + f'?page={i}' + \
                        '&parent_url_id=os27505&pay_type_ids=2&currency_alias=rur&price_term_lease=all_month&order_field=order_price_asc'

                    soup = self.getsoup(url)
                    
                    offers = soup.select("a[class = 'app-filter__sort-content-item']")
                    url_offers = [a.get('href') for a in offers]
                    urls += url_offers
        #             print(f'{url} собрано {len(url_offers)}')
            else:   
                offers = soup.select("a[class = 'app-filter__sort-content-item']")
                url_offers = [a.get('href') for a in offers]
                urls += url_offers
        #         print(f'{len(url_offers)}')
                    
        return urls


