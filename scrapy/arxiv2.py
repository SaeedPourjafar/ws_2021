# To run this file please put it in the spiders folder and run the code below in terminal/cmd:
# scrapy crawl computer -o computer.csv

import scrapy
from scrapy.exceptions import CloseSpider # To control the output of 100 results limit
import psutil # For memory usage
import os

limit = True # The default parameter for limiting the output to 100 results

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksSpider(scrapy.Spider):

    name = 'computer'
    allowed_domains = ['https://arxiv.org/']
    try:
        with open("topics.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    N = 100 # Setting the limit for number of pages
    count = 0 # Counting the pages
    def parse(self, response):
        print(response)
        # Extracting the link for every paper
        xpath = '//a[re:test(@title, "Abstract")]/@href'
        selection = response.xpath(xpath)
        # This block of code will be executed if the limit is set to True (default)
        if limit: 
            for s in selection:
                if self.count >= self.N:
                    # Closing the spider if it reaches the limit
                    raise CloseSpider(f"Scarped {self.N} items. Eject!") 
                self.count += 1 
                l = Link()
                l['link'] ='https://arxiv.org' + s.get()
                print(l)
                yield l
        # Or this if the limit is set to False
        else:
            for s in selection:
                l = Link()
                l['link'] ='https://arxiv.org' + s.get()
                print(l)
                yield l
    print("Memory usage in MB:",round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2))
