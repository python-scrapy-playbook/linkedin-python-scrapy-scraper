import logging
import scrapy
from spiders import configs
from spiders import iofunctions
from spiders import jobinfos

class JobDescriptionSpider(scrapy.Spider):
    name = "job_description_spider"
    logging.basicConfig(
        filename=f'{name}.log',
        filemode='w',
        level=logging.DEBUG,
        format=configs.LOG_FORMAT
    )

    logger = logging.getLogger(f'{name}')
    def __init__(self, job_id=None, output=None, **kwargs):
        super().__init__(**kwargs)
        self.job_id = job_id
        self.output = output
    
    def start_requests(self):
        self.logger.info("Start Requests.")
        yield scrapy.Request(url=f"{configs.JOB_URL_PREFIX}{self.job_id}/", headers=configs.HEADERS.copy(), callback=self.save_html_response)

    def save_html_response(self, response):
        self.logger.info("Saving Response as HTML.")
        iofunctions.save_html_response(response)
        return self.extract_job_infos(response)

    def extract_job_infos(self, reponse: bytes):
        self.logger.info("Extracting the Job infos.")
        job_infos = jobinfos.get_all_infos(reponse, self.job_id)
        iofunctions.save_json(job_infos)
        job_infos["collectedStatus"] = 200
        yield self.output_callback(job_infos)
    
    


    







        

    

