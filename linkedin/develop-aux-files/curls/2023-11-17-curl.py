import requests

cookies = {
    'JSESSIONID': 'ajax:3719889313256529511',
    'lang': 'v=2&lang=pt-br',
    'bcookie': '"v=2&55e1e7b9-322b-4cb4-8ab8-a38dfb2f971f"',
    'bscookie': '"v=1&20231117224235b12acba9-4b6c-461a-8123-1f9e144c5100AQEfoa7kPQz3P9RHJZT7HAcn3uZNxesQ"',
    'lidc': '"b=TGST01:s=T:r=T:a=T:p=T:g=3179:u=1:x=1:i=1700260955:t=1700347355:v=2:sig=AQHSrvA7jrTtyYfoLfNWhO1o4mg9KnxB"',
    'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
    'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-637568504%7CMCIDTS%7C19679%7CMCMID%7C22660077356991595700724586440625793758%7CMCAAMLH-1700865756%7C4%7CMCAAMB-1700865756%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1700268156s%7CNONE%7CvVersion%7C5.1.1',
    'aam_uuid': '22870778981405352570774919010094569749',
    '_gcl_au': '1.1.330205094.1700260957',
    '_uetsid': '9b19b5b0859a11eea4019b616c2f2585',
    '_uetvid': '9b19d5f0859a11eeb7121b3efa255689',
}

headers = {
    'authority': 'www.linkedin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


response = requests.get('https://www.linkedin.com/jobs/view/3738841851/', cookies=cookies, headers=headers)