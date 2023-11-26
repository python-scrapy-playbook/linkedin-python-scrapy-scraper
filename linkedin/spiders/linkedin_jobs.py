import scrapy
import logging
import time
from linkedin import configs

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
    logging.basicConfig(
        filename=f'{name}.log',
        filemode='w',
        level=logging.DEBUG,
        format=log_format
    )

    logger = logging.getLogger(f'{name}')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def start_requests(self):
        self.logger.info("Start requests")
        job_id_list = None
        with open(configs.PATH_JOBS_ID_LIST,"r") as job_ids:
            job_id_list = job_ids.readlines()
        self.logger.info("read job_list - ok")
        
        for job_id in job_id_list[0:1]:
            self.logger.info(f"making request for job_id {job_id}")
            yield scrapy.Request(url=f"{configs.JOB_URL_PREFIX}{job_id}/", headers=configs.HEADERS.copy(), callback=self.save_html)
    
    def get_job_id(self, response):
        self.logger.info("get job_id")
        job_url_splited = response.text.split(configs.JOB_URL_PREFIX)
        job_id = job_url_splited[1][0:10]
        return job_id
    
    def save_html(self, response):
        job_id = self.get_job_id(response)
        time.sleep(3)
        with open(f"{configs.PATH_JOBS_HTML_COLLECT}/job-{job_id}.html",'w') as job_file:
           job_file.writelines(response.text)
        self.logger.info("save html file - ok")    





        

    

