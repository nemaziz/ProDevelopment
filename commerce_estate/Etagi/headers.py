
import requests as rq
class headers_etagi:
    """Класс для обработки получения результата запроса
    функция parse_header"""
    
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


    def get_json(page: int, action = 'sale'):
        headers = f'''Accept:application/json
        Accept-Encoding:gzip, deflate
        Accept-Language:en-GB,en-US;q=0.9,en;q=0.8
        Content-Type:application/json; charset=utf-8
        Cookie:_ga_sync=wrokGmUsfMZUKwAIDfLaAg==; from_advertisement=false; visit_source=www.google.com; tmr_lvid=23d501c5fe0ba1b6c4f67a7eebb36a4e; tmr_lvidTS=1697414344398; _ym_uid=1697414344196302191; _ym_d=1697414344; emuuid=1b038b5f-da38-43fd-adf6-70a64d6a7f7e; olToken=a2f4992c-5224-4ebe-889b-e7b0dd80b31e; clbvid=652c7cc8d5e67b6d1ffc0d41; selected_city=spb; experimentUserID=0.6428574632204433; _gid=GA1.2.55422707.1698095112; _ym_isad=2; _ym_visorc=w; _ga=GA1.2.258751648.1697414344; tmr_detect=0%7C1698096179384; currentPageUrl=https%3A%2F%2Fspb.etagi.com%2Fcommerce%2F%3Fcity_id%5B%5D%3D1154%26city_id%5B%5D%3D1094%26city_id%5B%5D%3D2512%26city_id%5B%5D%3D2514%26city_id%5B%5D%3D242%26city_id%5B%5D%3D2028%26action_sl%3D{action}%26type%5B%5D%3Doffice%26type%5B%5D%3Dsklad%26type%5B%5D%3Dother%26type%5B%5D%3Dtorg%26type%5B%5D%3Ddev; _ga_34X0XLEBTX=GS1.1.1698094955.8.1.1698096536.0.0.0; _ga_YQCLPDPR4R=GS1.1.1698094955.8.1.1698096537.60.0.0; _gat_UA-54854319-18=1
        Referer:https://spb.etagi.com/commerce/?city_id[]=1154&city_id[]=1094&city_id[]=2512&city_id[]=2514&city_id[]=242&city_id[]=2028&action_sl=lease&type[]=office&type[]=sklad&type[]=other&type[]=torg&type[]=dev
        Sec-Ch-Ua:"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"
        Sec-Ch-Ua-Mobile:?0
        Sec-Ch-Ua-Platform:"Windows"
        Sec-Fetch-Dest:empty
        Sec-Fetch-Mode:cors
        Sec-Fetch-Site:same-origin
        User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'''

        

        headers = headers_etagi.parse_header(headers)
        
        #Мне не удалось, к сожалению, передавать параметры get запроса через аргумент data. Тогда этот url был бы понятнее.
        resp = rq.get(f'https://spb.etagi.com/rest/plugin.etagi?protName=commerceWithCharacteristics&fields&filter=%5B%22and%22%2C%5B%5B%22inOrEq%22%2C%22f.city_id%22%2C%5B1154%2C1094%2C2512%2C2514%2C242%2C2028%5D%5D%2C%5B%22%3D%22%2C%22f.action_sl%22%2C%22{action}%22%5D%2C%5B%22in%22%2C%22f.status%22%2C%5B%22active%22%2C%22sold%22%2C%22rent%22%2C%22rent_o_agency%22%5D%5D%2C%5B%22in%7C%3D%22%2C%22type%22%2C%5B%22office%22%2C%22sklad%22%2C%22other%22%2C%22torg%22%2C%22dev%22%5D%5D%5D%5D&order=%5B%22(CASE%20WHEN%20f.premium_status_id%20IN%20(224%2C227%2C278%2C280)%20THEN%201%20WHEN%20f.premium_status_id%20IN%20(225%2C228%2C279)%20THEN%202%20ELSE%20NULL%20END)%20ASC%20NULLS%20LAST%22%2C%22f.premium_start_max%20DESC%22%2C%22array_position(array%24%2Cf.object_id)%22%2C%22vladis_external_id%20desc%22%2C%22(visual%20is%20null)%22%2C%22f.prof_photo%3D%27f%27%22%2C%22f.date_update%20desc%22%2C%22f.object_id%20desc%22%5D&orderId=default&limit=30&offset={30*(page - 1)}&as=f&join&lang=ru&caseFilters=%7B%7D&bAddLimit=0&bIsFunction=0&cityId=242&module=with-nh-and-archive&countryISO=RU&sourceTable=etagi.offices&resetOrders=default&getAdvanced=true&withBotDescription=false&recommendedMode=client&domainId=242&valueToSort=%5B9402831%2C9546474%2C9997175%2C8813350%2C9246235%2C9789957%2C7551242%2C9291410%2C9882104%2C9513331%5D&count=1',
             headers = headers
             ).json()
        
        yield resp
        
