import requests as rq

class Headers_NF:
    def parse_header(self, raw_header: str):
        header = dict()
        for line in raw_header.split("\n"):
            if line.startswith(":"):
                a, b = line[1:].split(":", 1)
                a = f":{a}"
            else:
                a, b = line.split(":",1)
            header[a.strip()] = b.strip()
        return header

    def resp(self, url, source):
        headers = f"""Accept:application/json, text/plain, */*
        Accept-Encoding:gzip, deflate, br
        Accept-Language:ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
        Connection:keep-alive
        Cookie:vs_uuid=941cfc8211bd4327a623acc37ccff409; header_city=msk; _gid=GA1.2.1288467416.1691661027; _ym_uid=1691661027545251800; _ym_d=1691661027; tmr_lvid=1eb5168dd1d06976dba1636b2f37262a; tmr_lvidTS=1691661027456; _ymab_param=LcwzyXDOrrXh6E73ro4lTbpGmQJkmMyoNfjKD1LSCjk2viUngyCmDDq77Ju_zeQeMEog4eweu0Tnx-B6Mg609E4PKYA; _ym_isad=2; _ym_visorc=w; WhiteCallback_visitorId=13379283577; WhiteCallback_visit=22333278418; WhiteSaas_uniqueLead=no; _cmg_csstqw9ol=1691661032; _comagic_idqw9ol=7525344988.11051117673.1691661030; WidgetChat_invitation_2807478=true; WhiteCallback_mainPage=VlHrX; _ga_202TG0TXRL=GS1.1.1691661027.1.1.1691662105.60.0.0; _gat_UA-170074316-1=1; _gat_UA-82374931-1=1; _ga=GA1.1.1763772632.1691661027; WhiteCallback_openedPages=yxAvu.VpZxk; WhiteCallback_updateMainPage=yxAvu; _ga_395ML8WTE8=GS1.1.1691661027.1.1.1691662108.57.0.0; tmr_detect=0%7C1691662111628; WhiteCallback_timeAll=473; WhiteCallback_timePage=473; _gr_session=%7B%22s_id%22%3A%22756e3766-aee7-48de-8fb0-8935c6b83a69%22%2C%22s_time%22%3A1691662112822%7D
        Host:kf.expert
        Referer:{url}
        Sec-Ch-Ua:"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"
        Sec-Ch-Ua-Mobile:?0
        Sec-Ch-Ua-Platform:"Windows"
        Sec-Fetch-Dest:empty
        Sec-Fetch-Mode:cors
        Sec-Fetch-Site:same-origin
        User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"""

        headers = self.parse_header(headers)
        
        resp = rq.get(
            f"https://kf.expert{source}",
            headers=headers
        ).json()
        
        return resp