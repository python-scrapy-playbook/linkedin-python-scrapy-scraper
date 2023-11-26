import sys
import re
import os 
import unittest
import json
import pdb
from spiders import configs
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import NavigableString
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
    
    """
        Padrões:
        1 - negrito
        2 - 2 espaços antes
        3 - 2 pontos no final
        4 - negrito e sublinhado

    """

    def has_p_tag():
        pass

    def has_br_tag():
        pass

    def is_strong_upper():
        pass

    def is_title_description_tag(self, tag):
        #pdb.set_trace()
        if tag.previous_sibling == tag and isinstance(tag.next_sibling, NavigableString):
            return tag
        if tag.name == 'br' and isinstance(tag.next_sibling, NavigableString):
            tag_next_sibling = tag.next_sibling
            return tag_next_sibling 
        if isinstance(tag.previous_element, NavigableString) and tag.name == 'br':
            tag_next_sibling = tag.previous_element
            return tag_next_sibling
        else:
            #pdb.set_trace()
            None
    
    def is_description(self, description):

        name = description.name
        text = description.text
        
        if text and name == 'strong' and len(text) > 5 and  len(text) < 29:
            return description.text
        
        tag_text = description.next_sibling
        if len(tag_text) > 5 and len(tag_text) < 29:
            return tag_text.text
    
    def debug_p_test(self, description_title_tag):
        for tag in description_title_tag:
            
            if self.is_description(tag):
                print(self.is_description(tag))
    
    def get_next_element_recursive(self, div):
        div_text = div.text
        if div.next_element.name is not None:
            return div_text
        #pdb.set_trace()
        div_text = div_text + self.get_next_element_recursive(div.next_element)
        return div_text

    def remove_tags(self, div_tag):
        for div in div_tag.find_all("p"):
            div.unwrap()
        for div in div_tag.find_all("em"):
            div.unwrap()
        for div in div_tag.find_all("strong"):
            div.unwrap()
        for div in div_tag.find_all("ul"):
            div.unwrap()
        for div in div_tag.find_all("li"):
            div.unwrap()
        for div in div_tag.find_all("br"):
            div.unwrap()
    def get_all_text(self, div):
        pass

    def get_title_description_jobs(self, div, tag_find=['']):
        div_find = div.find_all(tag_find)
        description_title_tag=[]
        for index, strong_tag in enumerate(div_find):
            if self.is_title_description_tag(strong_tag) is not None:
                atual_tag = self.is_title_description_tag(strong_tag)
                description_title_tag.append(atual_tag)
        #description_title_tag_clear = list(filter(lambda x: x is not None, description_title_tag))
        #pdb.run(self.debug_p_test(description_title_tag))
        return description_title_tag

    def get_infos(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(class_=re.compile(configs.RE_CLASS_NAME))

        self.remove_tags(div)
        infos_obj = {}
        '//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div/text()[1]'
        '//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div/strong[2]'
        #print(f'LEN-STRONG: {len(strong_list)}')
        #raise KeyError
        
        strong_list_clear = self.get_title_description_jobs(div, ['br'])

        list_description = []
        for description in strong_list_clear:
            if description.name == 'br':
                description_concat = self.get_next_element_recursive(description)
                #print(description_concat)
                list_description.append(description_concat)
            else:
                list_description.append(description.text)
        pdb.set_trace()
        # if strong_list_clear == []:
        #     strong_list_clear = self.get_title_description_jobs(div, ['p','strong'])
        #
        print(f'LEN-STRONG-CLEAR: {len(list_description)}')
        last_text = ''
        for index, string_tag_clean in enumerate(list_description):    
            
            if index < len(list_description)-1 and string_tag_clean not in last_text:
                print(index)
                print(string_tag_clean)
                print("--------------")
                last_text = string_tag_clean
            if index == len(strong_list_clear)-1:
                print(string_tag_clean)
            
                #pdb.set_trace()
            # if isinstance(next_text, NavigableString):
            #     print(next_text)
            
            #uls = strong_tag.find("br")
            #print(uls)
        #     if uls == []:
        #         uls = strong_tag.next_sibling
            
        #     infos_obj[strong_tag.text] = []
        #     for ul in uls:
        #         lis = [] if not isinstance(ul,Tag) else ul.find_all('li')
        #         if lis == []:
        #             break
        #         for li in lis:
        #             infos_obj[strong_tag.text].append(li.text)
        
        # out_file = open("output.json", "w")
        # json.dump(infos_obj, out_file, indent = 4)
        # out_file.close() 
    
    #@unittest.skip("")
    def test_parser_description(self):
        files = self.get_job_files()
        for file in files[-36:-35]:
            print(file)
            response = self.read_file(file)
            self.get_infos(response)
    
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