import os 
import pdb
import sys
import unittest
from spiders import configs
from spiders import jobinfos
from scrapy.http import HtmlResponse
sys.dont_write_bytecode = True

class TestUnit(unittest.TestCase):
    def read_file(self, file_path):
        response = None
        with open(file_path,'r') as html_response:
            _body = html_response.read()
            response = HtmlResponse(url=file_path,body=_body, encoding='utf-8')
        return response
    
    def get_job_files(self):
        job_files = os.listdir(configs.PATH_JOBS_HTML_COLLECT)
        full_job_files = [f"{configs.PATH_JOBS_HTML_COLLECT}/{job}" for job in job_files]
        return full_job_files
    
    def get_html_files_test(self, index_initial=0, index_final=1):
        files = self.get_job_files()
        for file in files[index_initial:index_final]:
            print(file)
            response = self.read_file(file)
        return response
    
    #@unittest.skip("")
    def test_parser_description(self):
        response = self.get_html_files_test()
        text_job_description_result = jobinfos.get_text_job_description(response)
        pdb.set_trace()

    @unittest.skip("")
    def test_parser_job_title(self):
        response = self.get_html_files_test()
        tag_class_find = self.find_class(response, "top-card-layout__title")
        job_title_text = tag_class_find.text
        #pdb.set_trace()
    
    @unittest.skip("")
    def test_parser_job_company(self):
        response = self.get_html_files_test()
        re_class_find = "topcard__org-name-link"
        tag_class_find = self.find_class(response, "topcard__org-name-link")
        job_company = tag_class_find.text
        pdb.set_trace()
    
    @unittest.skip("")
    def test_parser_job_locale(self):
        response = self.get_html_files_test()
        re_class_find = "topcard__flavor topcard__flavor--bullet"
        tag_class_find = self.find_class(response, re_class_find)
        job_locale = tag_class_find.text
        pdb.set_trace()
    
    @unittest.skip("")
    def test_parser_job_criteria_list(self):
        response = self.get_html_files_test()
        job_criteria_infos = self.get_job_criteria_infos(response)
        pdb.set_trace()
    
    @unittest.skip("")
    def test_read_list_jobs(self):
        job_list_read = None
        with open(configs.PATH_JOBS_ID_LIST,"r") as job_list:
            job_list_read = job_list.readlines()
        print(job_list_read)
    
    @unittest.skip("")
    def test_split_url(self):
        url = 'https://www.linkedin.com/jobs/view/3762626775/?refId=7584f83d-05b7-416f-aaa9-f6b1aca96944&trackingId=MwJx8N6oTOS7ly4glqWqIQ%3D%3D&trk=flagship3_job_home_savedjobs'
        id_job = url.split("https://www.linkedin.com/jobs/view/")
        print("\n")
        print(id_job[1][0:10])
    
    @unittest.skip("")
    def test_list_dir(self):
        full_path = "/home/linkedin-python-scrapy-scraper/linkedin/test/curls/html_results"
        job_files = os.listdir("/home/linkedin-python-scrapy-scraper/linkedin/test/curls/html_results")

        for job in job_files:
            print(f"{full_path}{job}")

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)