import json
import scrapy

class LinkedCompanySpider(scrapy.Spider):
    name = "linkedin_company_profile"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start=' 

    #add your own list of company urls here
    company_pages = [
        'https://www.linkedin.com/company/usebraintrust?trk=public_jobs_jserp-result_job-search-card-subtitle',
        'https://www.linkedin.com/company/centraprise?trk=public_jobs_jserp-result_job-search-card-subtitle'
        ]


    def start_requests(self):
        
        company_index_tracker = 0

        #uncomment below if reading the company urls from a file instead of the self.company_pages array
        # self.readUrlsFromJobsFile()

        first_url = self.company_pages[company_index_tracker]

        yield scrapy.Request(url=first_url, callback=self.parse_response, meta={'company_index_tracker': company_index_tracker})


    def parse_response(self, response):
        company_index_tracker = response.meta['company_index_tracker']
        print('***************')
        print('****** Scraping page ' + str(company_index_tracker+1) + ' of ' + str(len(self.company_pages)))
        print('***************')

        company_item = {}

        company_item['name'] = response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip()
        company_item['summary'] = response.css('.top-card-layout__entity-info h4 span::text').get(default='not-found').strip()

        try:
            ## all company details 
            company_details = response.css('.core-section-container__content .mb-2')

            #industry line
            company_industry_line = company_details[1].css('.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()

            #company size line
            company_size_line = company_details[2].css('.text-md::text').getall()
            company_item['size'] = company_size_line[1].strip()

            #company founded
            company_size_line = company_details[5].css('.text-md::text').getall()
            company_item['founded'] = company_size_line[1].strip()
        except IndexError:
            print("Error: Skipped Company - Some details missing")

        yield company_item
        

        company_index_tracker = company_index_tracker + 1

        if company_index_tracker <= (len(self.company_pages)-1):
            next_url = self.company_pages[company_index_tracker]

            yield scrapy.Request(url=next_url, callback=self.parse_response, meta={'company_index_tracker': company_index_tracker})

    



    def readUrlsFromJobsFile(self):
        self.company_pages = []
        with open('jobs.json') as file:
            jobsFromFile = json.load(file)

            for job in jobsFromFile:
                if job['company_link'] != 'not-found':
                    self.company_pages.append(job['company_link'])
            
        #remove any duplicate links - to prevent spider from shutting down on duplicate
        self.company_pages = list(set(self.company_pages))
            
