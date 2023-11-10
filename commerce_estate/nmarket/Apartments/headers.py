import requests as rq
from get_keys import Keys_class
import json


key = Keys_class()

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

auth = None
def head(url):
    global auth
    if auth == None:
        auth = key.offers_get_key()
    
    headers = f"""Accept:application/json, text/plain, */*
    Accept-Encoding:gzip, deflate, br
    Accept-Language:en-GB,en-US;q=0.9,en;q=0.8
    Authorization:{auth}
    Content-Length:202
    Content-Type:application/json
    Cookie:SiteViewMode2=1; BrowserGuid=aa146c53-c8d2-482b-85c8-9f3af9ce372e; mycookies=iisbrokerage3.nmarket.local; _ym_uid=1691571020428130640; _ym_d=1691571020; _ym_isad=2; tmr_lvid=fe6a1cf19c1c194b1c768cf5c9f0e9dd; tmr_lvidTS=1691571019924; ClientRegionGroupId5=78; nmarketAuth=2OW5-9SyAfd8RZqVDSnHhcBuzdP5rX5RWjMOcf4WEz2nPm8k11l4x4BDG4CqXYjz7JGGkV0WvP4Pp5C8QvK2BrNxVKTfdqYHkvYm6c1DKOMghIFcxlGgdoYVCuh8kMswVSi5MV93ZbMH064hCe7opx0RqK2d8oi5SmPU79YQA4iHXw0Ph6R_b8ZGwMtm79lixkBQcUouO4cocFMaTgX_POqWgAkvevz6yiFng1_QzYoj60nmARbqMnHAQ9QDjqOWUftZC-IN8JfoHE-dT48NG-xgj7zDNGS3gD57Lf0cmLm_VSqI1kxlXg_wNF65bn3oq6HYUhKKAZzzlT8rS3aRgAXSMTO4N8OHQR9vsobW5Ywd4caLiX5zjjCXGzbGpFg_vq8hfoNdfzW__cTn_2Y7HQ; __RequestVerificationToken=aRcWom33y15GmukjX4Jz0z1Knu3Rc8MdRK3cSBNK2ADaOMe_kCA0J_0DF4FaQScjZK-sBi8hvrHl4qnGoGUcjNrxiXeNjPK0yC3iyh9EaGw1; pin-spa="3e0fe2e386441bf3"; sawBasketOnboarding=1; _gid=GA1.2.894531812.1691571278; _ga_3K9MRCZ3L3=GS1.2.1691571278.1.0.1691571278.60.0.0; _ga=GA1.1.1612324669.1691571020; search-control.isSmartLineMode=false; search-control.stopAnimation=1; userId=190262; arr_img=d55ae7137728c00475237f7f83066eca6d931993005858d6c739a17327d35362; _ga_SJBMT5GXF3=GS1.1.1691574187.2.1.1691575725.0.0.0; UserLastEnter=1691575727378
    Origin:https://spb.nmarket.pro
    Referer:{url}
    Sec-Ch-Ua:"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"
    Sec-Ch-Ua-Mobile:?0
    Sec-Ch-Ua-Platform:"Windows"
    Sec-Fetch-Dest:empty
    Sec-Fetch-Mode:cors
    Sec-Fetch-Site:same-origin
    User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"""

    headers = parse_header(headers)
    
    return headers

auth_pers = None
def rom(rr):    
    rid = rr.split('/')[-1]
    url = f'https://spb.nmarket.pro/presentation-new/api/presentation/realtyobject/{rid}'
    
    global auth_pers
    if auth_pers == None:
        auth_pers = key.pers_get_key(rid)
    
    headers = f"""Accept:application/json, text/plain, */*
    Accept-Encoding:gzip, deflate, br
    Accept-Language:ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
    Authorization:{auth_pers}
    Cookie:SiteViewMode2=1; BrowserGuid=91745c03-3cd8-4b59-b3b2-b9b800008f55; mycookies=iisbrokerage2.nmarket.local; _ym_uid=1683712500808365417; _ym_d=1683712500; tmr_lvid=6b49e24060a71321cff7511df976c64d; tmr_lvidTS=1683712500393; __RequestVerificationToken=M4N_CPzy1ASdUKMdnS__jy0WDb_rfp0WiqQ6dtI1IPs0Dp__0MPTZVxAMtfFrL_u2tnOxAX3oKO7QSRIvSOk5wR5LJaWBd9ZU-5PTBznSm41; pin-spa="ac6a35585d7637b7"; sawBasketOnboarding=1; search-control.isSmartLineMode=false; search-control.stopAnimation=1; cookie-banner=1; popupsmart_55452_session_popup_display_count=0; popupsmart_55452_popup_display_count=0; popupsmart_55452_popup_clicked_close=false; arr_img=da71091fc2d9bf74b379001e74e80a0c0cd2bfb18ce5164b353ce44a46d0026a; ClientRegionGroupId5=78; _ym_isad=2; nmarketAuth=lUkETm1inCuOebYa-TezBxhC_W8-ZzqTNsjn3UIjg5u9rUEWWgTp3STZ5CpoyBzNNO_TCf72quJLmyu2vxqpgQTzOr2qk3QoNeXsQvpJHXTL5ym5gWnSi7AeUS9hTi8Cxlgev_PXgR9hSU8PxRIufNIOVXkLnW0Zwjo3CMzcHQPFBsBuQDa8ZRzZ9jQVDpIrGPU5dbk7PzjmgaYOr6cpBA-MyMHDIqyQNsfv4-NT1jVpKLw2zxkUh75kDniZM4m7A8sjZX2YpLMfws9D19JiuvmxPxwa2tvH1hNGVyRz7LzdnuCo-YHzJriIOX_rlF2jxagdtGELuKijchdgK-RJwF1cX3qoDeRcpH3XWxj3Bhif3eMITYfeFslUThq3GMVu2V-k639CYq9zk6_xqyyBq2w0PvmK7xMGlWKePNnts9w; popupsmart_53768_visit_count=133; popupsmart_55452_visit_count=133; popupsmart_53768_session_popup_display_count=1; popupsmart_53768_popup_display_count=1; popupsmart_53768_last_display_date=2023-05-30T10:03:20.020Z; popupsmart_53768_popup_clicked_close=true; userId=undefined; _gid=GA1.2.1694089125.1685445261; _ga=GA1.1.263748218.1683712500; _ga_SJBMT5GXF3=GS1.1.1685443945.40.1.1685445897.0.0.0; UserLastEnter=1685445898783
    Referer:https://spb.nmarket.pro/presentation-new/realtyobject/{rid}
    Sec-Ch-Ua:"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
    Sec-Ch-Ua-Mobile:?0
    Sec-Ch-Ua-Platform:"Windows"
    Sec-Fetch-Dest:empty
    Sec-Fetch-Mode:cors
    Sec-Fetch-Site:same-origin
    Selectedregiongroupid:78
    User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"""
    
    headers = parse_header(headers)
    
    dt = rq.get(url,
               headers = headers).json()
    
    return dt

def resp(url, source, page, hs = False):

    
    payload = {
        "pageNumber": page,
        "pageSize": 30,
        "sorting": [
            {"name": "roomsSort", "sortOrder": 0},
            {"name": "houseShortNameString", "sortOrder": 0},
            {"name": "negotiatedPrice", "sortOrder": 1},
            {"name": "priceTotal", "sortOrder": 0}
        ]
    }
    
    if hs:
        payload = {
            "pageNumber":page,
            "pageSize":15
        }
    
    resp = rq.post(
        f"{source}",
        headers=head(url),
        data=json.dumps(payload)
    ).json()['data']
    
    return resp

authjk = None
def jk_data(jk_id):
    
    if '/' in jk_id:
        jk_id = jk_id.split('/')[-1]
    
    global authjk
    if authjk == None:
        authjk = key.house_get_key(jk_id = jk_id)
    
    headers = f"""Accept:application/json, text/plain, */*
    Accept-Encoding:gzip, deflate, br
    Accept-Language:en-GB,en-US;q=0.9,en;q=0.8
    Authorization:{authjk}
    Cookie:SiteViewMode2=1; BrowserGuid=be2fbbd8-d66c-4293-8e9e-b2c2766f70b5; _ym_uid=1696336830705467268; _ym_d=1696336830; tmr_lvid=55458d73e6c908f2f7ddcb383c191519; tmr_lvidTS=1696336829999; ClientRegionGroupId5=78; sawBasketOnboarding=1; _ga_828BSYD1ZZ=GS1.1.1696336962.1.1.1696337021.0.0.0; _ga_LZG5GFV1ZM=GS1.2.1696337283.1.0.1696337289.0.0.0; _ga=GA1.1.979756628.1696336830; __RequestVerificationToken=r1Zkzqs-6gjBR_Iq1TMW1ZHlNK3vPHvsTEBEsXiZbixeqBCj-Dp8W14MeG1keLY5TD-RyQUJcJRuZF9J2uZAqo9fwP_CZXAY7Q1AnA1vdgw1; mycookies=iisbrokerage1.nmarket.local; pin-spa="758f33ce2dc6e924"; _ym_isad=2; tmr_detect=0%7C1699554817410; nmarketAuth=AvdE7Nz8Ok2fxe8JyVoKP9t5InWmmuf1BioFPOElvIUvQIS-Os1KwXrSSAPfXzVb4Ajl9heJIImmAJC3N69IJFfD1q9iSkA7hc6D6b4sNRPjM_QvEb4La6MbZWT2fn36iF8jDpWfyLgpdiscH3KjNKw2fKYQ2xDCjNcZ0wxho_xQvL5sgMA7JlsJZjGSJQofDWHfg3scTpQpz_JFe0SXDrlRMIuUAz38QmsI1lHsFhIKNE9vOP4meCoO7KTztHEtX7oMxR-xTTyb4z7Tmn9du-t01RQJCp-93k4qD4xde6llUFNgRaCS4Ftwix1Hxi_rzZDJ9xnzVNbxPEFv3JWOeQBIyUV4RT5l2oiQhjcQQ7eQBC1VSUCAWDzpGbgCbYw1-VPSxgfbp2itSV71cnNI3Q; mindboxDeviceUUID=b56dd23e-724c-4297-af33-495e59bce1df; directCrm-session=%7B%22deviceGuid%22%3A%22b56dd23e-724c-4297-af33-495e59bce1df%22%7D; arr_img=d55ae7137728c00475237f7f83066eca6d931993005858d6c739a17327d35362; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ga_J0LB3YXCJ8=GS1.1.1699554830.1.1.1699554831.0.0.0; userId=190262; _ga_SJBMT5GXF3=GS1.1.1699554815.3.1.1699555894.0.0.0; UserLastEnter=1699555895440
    Referer:https://spb.nmarket.pro/search/complex/86712?isSmartLineMode=false&searchString=%7B%22TTypeObjNewBuildId%22:%5B%221%22,%222%22%5D%7D
    Sec-Ch-Ua:"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
    Sec-Ch-Ua-Mobile:?0
    Sec-Ch-Ua-Platform:"Windows"
    Sec-Fetch-Dest:empty
    Sec-Fetch-Mode:cors
    Sec-Fetch-Site:same-origin
    User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"""

    headers = parse_header(headers)

    url = f'https://spb.nmarket.pro/complex/GetComplexInfo?complexId={jk_id}'

    dt = rq.get(url,
                headers = headers
               ).json()
    
    
    return dt

