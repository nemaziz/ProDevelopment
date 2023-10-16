

def get_json(page):
    headers = f"""Accept:application/json
    Accept-Encoding:gzip, deflate, br
    Accept-Language:en-GB,en-US;q=0.9,en;q=0.8
    Content-Type:application/json; charset=utf-8
    Cookie:_ga_sync=wrokGmUsfMZUKwAIDfLaAg==; from_advertisement=false; visit_source=www.google.com; _gid=GA1.2.769756332.1697414344; tmr_lvid=23d501c5fe0ba1b6c4f67a7eebb36a4e; tmr_lvidTS=1697414344398; _ym_uid=1697414344196302191; _ym_d=1697414344; emuuid=1b038b5f-da38-43fd-adf6-70a64d6a7f7e; _ym_isad=2; olToken=a2f4992c-5224-4ebe-889b-e7b0dd80b31e; clbvid=652c7cc8d5e67b6d1ffc0d41; selected_city=spb; experimentUserID=0.6428574632204433; _ym_visorc=w; em_recommended_objects=empty; v1_data=; currentPageUrl=https%3A%2F%2Fspb.etagi.com%2Fcommerce%2F%3Fcity_id%5B%5D%3D242%26city_id%5B%5D%3D1154%26city_id%5B%5D%3D1094%26city_id%5B%5D%3D2512%26city_id%5B%5D%3D2514%26city_id%5B%5D%3D2028%26type%5B%5D%3Doffice%26page%3D1; v1_referrer_callibri=; tmr_detect=0%7C1697460630291; _ga=GA1.2.258751648.1697414344; _ga_34X0XLEBTX=GS1.1.1697458572.2.1.1697460808.0.0.0; _ga_YQCLPDPR4R=GS1.1.1697458572.2.1.1697460808.60.0.0; _gat_UA-54854319-18=1
    Referer:https://spb.etagi.com/commerce/?city_id[]=242&city_id[]=1154&city_id[]=1094&city_id[]=2512&city_id[]=2514&city_id[]=2028&type[]=office&page={page}
    Sec-Ch-Ua:"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"
    Sec-Ch-Ua-Mobile:?0
    Sec-Ch-Ua-Platform:"Windows"
    Sec-Fetch-Dest:empty
    Sec-Fetch-Mode:cors
    Sec-Fetch-Site:same-origin
    User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"""

    headers = parse_header(headers)

    resp = rq.get(f'''https://spb.etagi.com/rest/plugin.etagi?protName=commerceWithCharacteristics&fields&filter=%5B%22and%22%2C%5B%5B%22inOrEq%22%2C%22f.city_id%22%2C%5B242%2C1154%2C1094%2C2512%2C2514%2C2028%5D%5D%2C%5B%22%3D%22%2C%22f.action_sl%22%2C%22sale%22%5D%2C%5B%22in%22%2C%22f.status%22%2C%5B%22active%22%2C%22sold%22%2C%22rent%22%2C%22rent_o_agency%22%5D%5D%2C%5B%22in%7C%3D%22%2C%22type%22%2C%5B%22office%22%5D%5D%5D%5D&order=%5B%22(CASE%20WHEN%20f.premium_status_id%20IN%20(224%2C227%2C278%2C280)%20THEN%201%20WHEN%20f.premium_status_id%20IN%20(225%2C228%2C279)%20THEN%202%20ELSE%20NULL%20END)%20ASC%20NULLS%20LAST%22%2C%22f.premium_start_max%20DESC%22%2C%22array_position(array%24%2Cf.object_id)%22%2C%22vladis_external_id%20desc%22%2C%22(visual%20is%20null)%22%2C%22f.prof_photo%3D%27f%27%22%2C%22f.date_update%20desc%22%2C%22f.object_id%20desc%22%5D&orderId=default&limit=30&offset={30 * (page - 1)}&as=f&join&lang=ru&caseFilters=%7B%7D&bAddLimit=0&bIsFunction=0&cityId=242&module=with-nh-and-archive&countryISO=RU&sourceTable=etagi.offices&resetOrders=default&getAdvanced=true&withBotDescription=false&recommendedMode=client&domainId=242&count=1''',
        headers=headers
    ).json()
    
    return resp