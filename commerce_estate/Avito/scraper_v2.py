import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import json

base_url = lambda page: 'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?p={}'.format(page)

class scraper:
    
    def __init__(self) -> None:
        self.session = rq.Session()
        
    def parse_header(self, raw_header: str) -> str:
        header = dict()
        for line in raw_header.split("\n"):
            if line.startswith(":"):
                a, b = line[1:].split(":", 1)
                a = f":{a}"
            else:
                a, b = line.split(":",1)
            header[a.strip()] = b.strip()
        return header
    
    def get_json(self, limit, page):
        url = base_url(page)
        
        headers = f"""Accept:application/json
                    Accept-Encoding:gzip, deflate, br
                    Accept-Language:ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
                    Cookie:srv_id=_in8v3cPGv439F1t.pv8DEvFEE2qCTRTC8mocn506JPVjab2MGLRnCDcC0BKVBqY7wqbkGy1pHnbJPoo=.sKLm4xKVnEfbYMzYsHZIYcXfPt2soPgWhVLiJ35htyE=.web; u=2y7rcusd.psxc9a.1lc4q5ogi2900; _gcl_au=1.1.756407875.1702044174; _ga=GA1.1.1628045832.1702044174; tmr_lvid=2b65124eda4cc7012869344c58428214; tmr_lvidTS=1702044174392; _ym_uid=1702044175999009250; _ym_d=1702044175; adrcid=AUMnqFXmD8Y1OXl_jYF1hSw; uxs_uid=7c247960-95d2-11ee-9f59-ada3bc1b2bbc; buyer_laas_location=653240; __upin=d9SIlydAFpwg49C6OdieBw; buyer_location_id=653240; advcake_track_id=03f481af-25e4-34b8-3e37-42c34278f6ad; advcake_session_id=0c37e19c-d627-d42d-e066-580d5044fbcf; SEARCH_HISTORY_IDS=1; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyU2F0JTJDJTIwMDElMjBGZWIlMjAyMDI1JTIwMTElM0EzMyUzQTM4JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMjM5ZTgwMTJkYzhhNmVkMWZmNDg1ZmY3Y2ZkMTk2Nzk3JTVDJTIyJTJDJTVDJTIyYnJvd3NlclZlcnNpb24lNUMlMjIlM0ElNUMlMjIxMjAuMCU1QyUyMiU3RCUyMiU3RA==; _buzz_aidata=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyU2F0JTJDJTIwMDElMjBGZWIlMjAyMDI1JTIwMTElM0EzMyUzQTM4JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMmQ5U0lseWRBRnB3ZzQ5QzZPZGllQnclNUMlMjIlMkMlNUMlMjJicm93c2VyVmVyc2lvbiU1QyUyMiUzQSU1QyUyMjEyMC4wJTVDJTIyJTdEJTIyJTdE; _ga_WW6Q1STJ8M=GS1.1.1707304257.7.0.1707304257.0.0.0; _ga_ZJDLBTV49B=GS1.1.1707304257.6.0.1707304257.0.0.0; v=1707397166; luri=sankt-peterburg; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d22ebf3cb6fd35a0ac8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c2da10fb74cac1eab2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642baf80da35caa52287658d123ba269e03698919b43d464ea855470c335d97c1154525907271a6a0eb69a2241f7870d4d8f4857885524eb1f691e52da22a560f550df103df0c26013a0df103df0c26013aaaa2b79c1ae92595e4be01cb553df4c5a0a556dd18608e213de19da9ed218fe2c772035eab81f5e123f5e56da7ec04f4a1a4201a28a6ec9b059080ed9becc4cd; ft="ntKcZAs+1DAJ8ZE5UDpyZtENX8Shro53bwYof4eAv6npmPZLVZsIOVZZReRHLHG4hLV9vWsRWhvwFFE0uaoc7CalmCvc6jw1LVr7v5qvTu1lt6a33WfUS4+v7GS+KO+zT6WLJJKLUKQ/lzwoQI60jQsDegN3f0JW/u/CtHYZC5/cgT1YiP5V2xQZ1scNCu9b"; _ym_isad=2; _ym_visorc=b; sx=H4sIAAAAAAAC%2FwTAMRICIQwF0Lv82iJsshvgNiKJ61gohQzKcHffhBqb%2Br4ndw1US0lsWyUy99smckWe6MgobM97O1OTdzx18CNyHx%2F%2Ftpf5ryouMOSgpBL5OMJa%2FwAAAP%2F%2FffYUBFsAAAA%3D; abp=0; _ga_M29JC28873=GS1.1.1707397167.20.1.1707397263.59.0.0; tmr_detect=0%7C1707397268861; buyer_from_page=map
                    Referer:{url}
                    Sec-Ch-Ua:"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
                    Sec-Ch-Ua-Mobile:?0
                    Sec-Ch-Ua-Platform:"Windows"
                    Sec-Fetch-Dest:empty
                    Sec-Fetch-Mode:cors
                    Sec-Fetch-Site:same-origin
                    User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
                    X-Requested-With:XMLHttpRequest
                    X-Source:client-browser"""
                    
        payload = {
            'categoryId': 42,
            'locationId': 653240,
            'correctorMode': 0,
            'page': 1,
            'map': 'eyJ6b29tIjo2fQ==',
            'params[536]': 5545,
            'verticalCategoryId': 1,
            'rootCategoryId': 4,
            'localPriority': 0,
            'disabledFilters[ids][0]': 'byTitle',
            'disabledFilters[slugs][0]': 'bt',
            'subscription[visible]': 'true',
            'subscription[isShowSavedTooltip]': 'false',
            'subscription[isErrorSaved]': 'false',
            'subscription[isAuthenticated]': 'false',
            'viewPort[width]': 500,
            'viewPort[height]': 748,
            'limit': limit,
            'countAndItemsOnly': 1
        }
                    
        headers = self.parse_header(headers)

        source = f'https://www.avito.ru/js/1/map/items?categoryId=42&locationId=653240&correctorMode=0&page={page}&map=eyJ6b29tIjo4fQ%3D%3D&params%5B536%5D=5545&verticalCategoryId=1&rootCategoryId=4&localPriority=0&disabledFilters%5Bids%5D%5B0%5D=byTitle&disabledFilters%5Bslugs%5D%5B0%5D=bt&viewPort%5Bwidth%5D=500&viewPort%5Bheight%5D=748&limit={limit}&countAndItemsOnly=1'

        resp = self.session.post(
            f"{source}",
            headers=headers,
            data=json.dumps(payload)
        )
        
        return resp
        
base_url = lambda page: 'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?p={}'.format(page)

def parse_header(raw_header: str):
    header = dict()
    for line in raw_header.split("\n"):
        if line.startswith(":"):
            a, b = line[1:].split(":", 1)
            a = f":{a}"
        else:
            a, b = line.split(":",1)
        header[a.strip()] = b.strip()
    return header

limit = 30
page = 1
url = base_url(page)
params = 5545

session = rq.Session()


payload = {
    'categoryId': 42,
    'locationId': 653240,
    'correctorMode': 0,
    'page': 1,
    'map': 'eyJ6b29tIjo2fQ==',
    'params[536]': params,
    'verticalCategoryId': 1,
    'rootCategoryId': 4,
    'localPriority': 0,
    'disabledFilters[ids][0]': 'byTitle',
    'disabledFilters[slugs][0]': 'bt',
    'subscription[visible]': 'true',
    'subscription[isShowSavedTooltip]': 'false',
    'subscription[isErrorSaved]': 'false',
    'subscription[isAuthenticated]': 'false',
    'viewPort[width]': 500,
    'viewPort[height]': 748,
    'limit': limit,
    'countAndItemsOnly': 1
}

headers = f"""Accept:application/json
Accept-Encoding:gzip, deflate, br
Accept-Language:ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
Cookie:srv_id=_in8v3cPGv439F1t.pv8DEvFEE2qCTRTC8mocn506JPVjab2MGLRnCDcC0BKVBqY7wqbkGy1pHnbJPoo=.sKLm4xKVnEfbYMzYsHZIYcXfPt2soPgWhVLiJ35htyE=.web; u=2y7rcusd.psxc9a.1lc4q5ogi2900; _gcl_au=1.1.756407875.1702044174; _ga=GA1.1.1628045832.1702044174; tmr_lvid=2b65124eda4cc7012869344c58428214; tmr_lvidTS=1702044174392; _ym_uid=1702044175999009250; _ym_d=1702044175; adrcid=AUMnqFXmD8Y1OXl_jYF1hSw; uxs_uid=7c247960-95d2-11ee-9f59-ada3bc1b2bbc; buyer_laas_location=653240; __upin=d9SIlydAFpwg49C6OdieBw; buyer_location_id=653240; advcake_track_id=03f481af-25e4-34b8-3e37-42c34278f6ad; advcake_session_id=0c37e19c-d627-d42d-e066-580d5044fbcf; SEARCH_HISTORY_IDS=1; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyU2F0JTJDJTIwMDElMjBGZWIlMjAyMDI1JTIwMTElM0EzMyUzQTM4JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMjM5ZTgwMTJkYzhhNmVkMWZmNDg1ZmY3Y2ZkMTk2Nzk3JTVDJTIyJTJDJTVDJTIyYnJvd3NlclZlcnNpb24lNUMlMjIlM0ElNUMlMjIxMjAuMCU1QyUyMiU3RCUyMiU3RA==; _buzz_aidata=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyU2F0JTJDJTIwMDElMjBGZWIlMjAyMDI1JTIwMTElM0EzMyUzQTM4JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMmQ5U0lseWRBRnB3ZzQ5QzZPZGllQnclNUMlMjIlMkMlNUMlMjJicm93c2VyVmVyc2lvbiU1QyUyMiUzQSU1QyUyMjEyMC4wJTVDJTIyJTdEJTIyJTdE; _ga_WW6Q1STJ8M=GS1.1.1707304257.7.0.1707304257.0.0.0; _ga_ZJDLBTV49B=GS1.1.1707304257.6.0.1707304257.0.0.0; v=1707397166; luri=sankt-peterburg; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d22ebf3cb6fd35a0ac8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c2da10fb74cac1eab2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642baf80da35caa52287658d123ba269e03698919b43d464ea855470c335d97c1154525907271a6a0eb69a2241f7870d4d8f4857885524eb1f691e52da22a560f550df103df0c26013a0df103df0c26013aaaa2b79c1ae92595e4be01cb553df4c5a0a556dd18608e213de19da9ed218fe2c772035eab81f5e123f5e56da7ec04f4a1a4201a28a6ec9b059080ed9becc4cd; ft="ntKcZAs+1DAJ8ZE5UDpyZtENX8Shro53bwYof4eAv6npmPZLVZsIOVZZReRHLHG4hLV9vWsRWhvwFFE0uaoc7CalmCvc6jw1LVr7v5qvTu1lt6a33WfUS4+v7GS+KO+zT6WLJJKLUKQ/lzwoQI60jQsDegN3f0JW/u/CtHYZC5/cgT1YiP5V2xQZ1scNCu9b"; _ym_isad=2; _ym_visorc=b; sx=H4sIAAAAAAAC%2FwTAMRICIQwF0Lv82iJsshvgNiKJ61gohQzKcHffhBqb%2Br4ndw1US0lsWyUy99smckWe6MgobM97O1OTdzx18CNyHx%2F%2Ftpf5ryouMOSgpBL5OMJa%2FwAAAP%2F%2FffYUBFsAAAA%3D; abp=0; _ga_M29JC28873=GS1.1.1707397167.20.1.1707397263.59.0.0; tmr_detect=0%7C1707397268861; buyer_from_page=map
Referer:{url}
Sec-Ch-Ua:"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
Sec-Ch-Ua-Mobile:?0
Sec-Ch-Ua-Platform:"Windows"
Sec-Fetch-Dest:empty
Sec-Fetch-Mode:cors
Sec-Fetch-Site:same-origin
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
X-Requested-With:XMLHttpRequest
X-Source:client-browser"""

headers = parse_header(headers)

headers = rq.utils.default_headers()
headers.update({'User-Agent': 'My User Agent 1.0',})

source = f'https://www.avito.ru/js/1/map/items?categoryId=42&locationId=653240&correctorMode=0&page={page}&map=eyJ6b29tIjo4fQ%3D%3D&params%5B536%5D={params}&verticalCategoryId=1&rootCategoryId=4&localPriority=0&disabledFilters%5Bids%5D%5B0%5D=byTitle&disabledFilters%5Bslugs%5D%5B0%5D=bt&viewPort%5Bwidth%5D=500&viewPort%5Bheight%5D=748&limit={limit}&countAndItemsOnly=1'

resp = session.post(
    f"{source}",
    headers=headers,
    data=json.dumps(payload)
)#.json()['data']


import cloudscraper
s = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0'})

url = 'https://www.avito.ru/web/1/main/items'
params = {
    'forceLocation': False,
    'locationId': 653040,
    'lastStamp': 1683748131,
    'limit': 30,
    'offset': 89,
    'categoryId': 4
}
r = s.get(url, params=params)
print(r)
    