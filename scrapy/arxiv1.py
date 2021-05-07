# Please note that since the number of topics in computer science are exactly 40 and it's less than 100
# therefore we applied the limit on the second file (arxiv2.py) which has somewhere around 700-800 outputs

# To run this file please put it in the spiders folder and run the code below in terminal/cmd:
# scrapy crawl topics -o topics.csv

import scrapy
import psutil # For memory usage
import os

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'topics'
    allowed_domains = ['https://arxiv.org']
    start_urls = ['https://arxiv.org']

    def parse(self, response):
        # We are looking for the list of topics under Computer Science section 
        # i.e. from 'Artificial Intelligence' all the way to 'Systems and Control'
        xpath = '//h2/following-sibling::h2[contains(text(),"Computer Science")]/following-sibling::ul/li/a[re:test(@id, "cs\..*")]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://arxiv.org' + s.get()
            yield l
    
    print("Memory usage in MB:",round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2))

