HEADERS = {
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

JOB_URL_PREFIX = "https://www.linkedin.com/jobs/view/"
PATH_JOBS_HTML_COLLECT = "/home/linkedin-python-scrapy-scraper/linkedin/tests/jobs_html_collected"
PATH_JOBS_JSON_COLLECT = "/home/linkedin-python-scrapy-scraper/linkedin/tests/jobs_json_collected"
PATH_JOBS_ID_LIST = "/home/linkedin-python-scrapy-scraper/linkedin/tests/jobs_id_list.txt"
RE_CLASS_NAME = "show-more-less-html"
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s:%(message)s"