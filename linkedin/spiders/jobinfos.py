import re
from bs4 import BeautifulSoup
from spiders import configs

def remove_tags(div_tag):
    tag_to_remove = ["p","u", "em", "strong", "ul", "li", "br"]
    for tag_remove in tag_to_remove:
        for tag in div_tag.find_all(tag_remove):
            tag.unwrap()
    
def create_soup(response):
    soup_response = BeautifulSoup(response.text, 'html.parser')
    return soup_response 
    
def find_class(soup_response, re_class_name):
    tag_find = soup_response.find(class_=re.compile(re_class_name))
    return tag_find
    
def get_text_job_description(soup_response):
    full_text = ''
    tag_class_find = find_class(soup_response, configs.RE_CLASS_NAME)
    div_tag = tag_class_find.find('div')
    remove_tags(div_tag)
    for text in div_tag:
        if text[0].isupper():
            full_text = f"{full_text}\n{text.strip()}"
        else:
            full_text = f"{full_text} {text.strip()}"
    return full_text
    
def get_job_criteria_infos(soup_response):
    re_class_find = "description__job-criteria-list"
    tag_class_find = find_class(soup_response, re_class_find)
    tag_span_list = tag_class_find.find_all("span")
    criteria_list = {
        "seniority_level":"",
        "employment_type":"",
        "job_function":"",
        "industries":"",
    }
    criteria_index = {
        0:"seniority_level",
        1:"employment_type",
        2:"job_function",
        3:"industries"
    }
    for index, tag_class_find in enumerate(tag_span_list):
        criteria_list[criteria_index.get(index)] = tag_class_find.text.strip()
    
    return criteria_list

def get_job_title(soup_response):
    tag_class_find = find_class(soup_response, "top-card-layout__title")
    job_title_text = tag_class_find.text
    return job_title_text.strip()

def get_job_company(soup_response):
    re_class_find = "topcard__org-name-link"
    tag_class_find = find_class(soup_response, re_class_find)
    job_company = tag_class_find.text
    return job_company.strip()

def get_job_locale(soup_response):
    re_class_find = "topcard__flavor topcard__flavor--bullet"
    tag_class_find = find_class(soup_response, re_class_find)
    job_locale = tag_class_find.text
    return job_locale.strip()
        
def get_all_infos(response, id):
    soup_response = create_soup(response)
    _id = id.strip()
    job_infos = {
        "id":_id,
        "title": get_job_title(soup_response),
        "company": get_job_company(soup_response),
        "locale": get_job_locale(soup_response),
        "description": get_text_job_description(soup_response),
        "criteria": get_job_criteria_infos(soup_response),
    }

    return job_infos

def get_job_id(response):
    job_url_splited = response.text.split(configs.JOB_URL_PREFIX)
    job_id = job_url_splited[1][0:10]
    return job_id
