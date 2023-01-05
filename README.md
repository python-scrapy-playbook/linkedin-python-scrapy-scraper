# linkedin-python-scrapy-scraper
Python Scrapy spiders that scrape job data & people and company profiles from [LinkedIn.com](https://www.linkedin.com/). 

This Scrapy project contains 3 seperate spiders:

| Spider  |      Description      |
|----------|-------------|
| `linkedin_people_profile` |  Scrapes people data from LinkedIn people profile pages. | 
| `linkedin_jobs` |  Scrapes job data from LinkedIn (https://www.linkedin.com/jobs/search) | 
| `linkedin_company_profile` |  Scrapes company data from LinkedIn company profile pages. | 


The following articles go through in detail how these LinkedIn spiders were developed, which you can use to understand the spiders and edit them for your own use case.

- [Python Scrapy: Build A LinkedIn.com People Profile Scraper](https://scrapeops.io/python-scrapy-playbook/python-scrapy-linkedin-people-scraper/)
- [Python Scrapy: Build A LinkedIn.com Jobs Scraper](https://scrapeops.io/python-scrapy-playbook/python-scrapy-linkedin-jobs-scraper/)
- [Python Scrapy: Build A LinkedIn.com Company Profile Scraper](https://scrapeops.io/python-scrapy-playbook/python-scrapy-linkedin-company-scraper/)

## ScrapeOps Proxy
This LinkedIn spider uses [ScrapeOps Proxy](https://scrapeops.io/proxy-aggregator/) as the proxy solution. ScrapeOps has a free plan that allows you to make up to 1,000 requests per month which makes it ideal for the development phase, but can be easily scaled up to millions of pages per month if needs be.

You can [sign up for a free API key here](https://scrapeops.io/app/register/main).

To use the ScrapeOps Proxy you need to first install the proxy middleware:

```python

pip install scrapeops-scrapy-proxy-sdk

```

Then activate the ScrapeOps Proxy by adding your API key to the `SCRAPEOPS_API_KEY` in the ``settings.py`` file.

```python

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

SCRAPEOPS_PROXY_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

```


## ScrapeOps Monitoring
To monitor our scraper, this spider uses the [ScrapeOps Monitor](https://scrapeops.io/monitoring-scheduling/), a free monitoring tool specifically designed for web scraping. 

**Live demo here:** [ScrapeOps Demo](https://scrapeops.io/app/login/demo) 

![ScrapeOps Dashboard](https://scrapeops.io/assets/images/scrapeops-promo-286a59166d9f41db1c195f619aa36a06.png)

To use the ScrapeOps Proxy you need to first install the monitoring SDK:

```

pip install scrapeops-scrapy

```


Then activate the ScrapeOps Proxy by adding your API key to the `SCRAPEOPS_API_KEY` in the ``settings.py`` file.

```python

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}


DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

```

If you are using both the ScrapeOps Proxy & Monitoring then you just need to enter the API key once.


## Running The Scrapers
Make sure Scrapy and the ScrapeOps Monitor is installed:

```

pip install scrapy scrapeops-scrapy

```

To run the LinkedIn spiders you should first set the search query parameters you want to search by updating the `profile_list` list in the spiders:

```python

def start_requests(self):
    profile_list = ['reidhoffman']
    for profile in profile_list:
        linkedin_people_url = f'https://www.linkedin.com/in/{profile}/' 
        yield scrapy.Request(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url})


```

Then to run the spider, enter one of the following command:

```

scrapy crawl linkedin_people_profile

```


## Customizing The LinkedIn People Profile Scraper
The following are instructions on how to modify the LinkedIn People Profile scraper for your particular use case.

Check out this [guide to building a LinkedIn.com Scrapy people profile spider](https://scrapeops.io/python-scrapy-playbook/python-scrapy-linkedin-people-scraper//) if you need any more information.

### Configuring LinkedIn People Profile Search
To change the query parameters for the people profile search just change the profiles in the `profile_list` lists in the spider.

For example:

```python

def start_requests(self):
    profile_list = ['reidhoffman', 'other_person']
    for profile in profile_list:
        linkedin_people_url = f'https://www.linkedin.com/in/{profile}/' 
        yield scrapy.Request(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url})

```

### Extract More/Different Data
LinkedIn People Profile pages contain a lot of useful data, however, in this spider is configured to only parse:

- Name
- Description
- Number of followers
- Number of connections
- Location
- About
- Experienes - organisation name, organisation profile link, position, start & end dates, description.
- Education - organisation name, organisation profile link, course details, start & end dates, description.

You can expand or change the data that gets extract by adding additional parsers and adding the data to the `item` that is yielded in the `parse_profiles` method:


### Speeding Up The Crawl
The spiders are set to only use 1 concurrent thread in the ``settings.py`` file as the ScrapeOps Free Proxy Plan only gives you 1 concurrent thread.

However, if you upgrade to a paid ScrapeOps Proxy plan you will have more concurrent threads. Then you can increase the concurrency limit in your scraper by updating the `CONCURRENT_REQUESTS` value in your ``settings.py`` file.

```python
# settings.py

CONCURRENT_REQUESTS = 10

```

### Storing Data
The spiders are set to save the scraped data into a CSV file and store it in a data folder using [Scrapy's Feed Export functionality](https://docs.scrapy.org/en/latest/topics/feed-exports.html).

```python

custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

```

If you would like to save your CSV files to a AWS S3 bucket then check out our [Saving CSV/JSON Files to Amazon AWS S3 Bucket guide here](https://scrapeops.io//python-scrapy-playbook/scrapy-save-aws-s3)

Or if you would like to save your data to another type of database then be sure to check out these guides:

- [Saving Data to JSON](https://scrapeops.io/python-scrapy-playbook/scrapy-save-json-files)
- [Saving Data to SQLite Database](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-sqlite)
- [Saving Data to MySQL Database](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-mysql)
- [Saving Data to Postgres Database](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres)

### Deactivating ScrapeOps Proxy & Monitor
To deactivate the ScrapeOps Proxy & Monitor simply comment out the follow code in your `settings.py` file:

```python
# settings.py

# SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

# SCRAPEOPS_PROXY_ENABLED = True

# EXTENSIONS = {
# 'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
# }

# DOWNLOADER_MIDDLEWARES = {

#     ## ScrapeOps Monitor
#     'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
#     ## Proxy Middleware
#     'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
# }



```

