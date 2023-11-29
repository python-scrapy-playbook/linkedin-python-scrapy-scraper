import unittest
from spiders import iofunctions
from spiders import configs
from spiders import job_description_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.JOB_ID_LIST = iofunctions.read_file(configs.PATH_JOBS_ID_LIST)
        self.outputs = []

    def output_callback(self, output_spider):
        self.outputs.append(dict(output_spider))
    
    def test_request_200(self):    
        test = 1
        for job_id in self.JOB_ID_LIST[test:test+1]:
            process = CrawlerProcess(get_project_settings())
            process.crawl(job_description_spider.JobDescriptionSpider, job_id, output_callback=self.output_callback)
            process.start() 
            self.assertEqual(self.outputs[0].get("collectedStatus"), 200)


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)