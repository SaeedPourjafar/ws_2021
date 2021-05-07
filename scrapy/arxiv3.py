# To run this file please put it in the spiders folder and run the code below in terminal/cmd:
# scrapy crawl papers -o papers.csv
import scrapy
import psutil # For memory usage
import os

class Papers(scrapy.Item):
    # Setting the feature to extract from every paper
    title        = scrapy.Field()
    category     = scrapy.Field()
    authors      = scrapy.Field()
    date         = scrapy.Field()
    pdf          = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'papers'
    allowed_domains = ['https://arxiv.org']
    # Specifying exported fields and their order in csv file
    custom_settings = {'FEED_EXPORT_FIELDS': ["title", "category","authors", "date", "pdf"],}
    try:
        with open("computer.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        p = Papers()

        title_xpath  = '//h1[@class = "title mathjax"]/text()'
        category_xpath= '//td[@class="tablecell arxivid"]/span/text()'
        authors_xpath= '//div[@class = "authors"]/a/text()'
        date_xpath   = '//div[@class = "submission-history"]/text()[4]'
        pdf_xpath    = '//a[text() = "PDF"]/@href'
        
        p['title']   = response.xpath(title_xpath).getall()
        
        if '[cs.' in response.xpath(category_xpath).getall()[0]:
            p['category']= response.xpath(category_xpath).getall()[0][-3:-1]
        else: # To make sure that it gets the CS tags if the paper is an interdisciplinary
            category_xpath = '//td[@class="tablecell subjects"]/text()'
            temp = response.xpath(category_xpath).getall()[-1].split(';')
            for i in temp:
                if '(cs.' in i:
                    p['category'] = i[-3:-1]

        p['authors'] = response.xpath(authors_xpath).getall()
        # Splitting the string and then grabbing the date of submission
        # Adding criteria
        if len(response.xpath(date_xpath).getall()[0]) < 4:
            date_xpath   = '//div[@class = "submission-history"]/text()[5]'
            p['date']    = '-'.join(response.xpath(date_xpath).getall()[0].split()[1:4])
        p['date']    = '-'.join(response.xpath(date_xpath).getall()[0].split()[1:4])

        # For handeling errors in which some pages denoted 'PDF only' instead of 'PDF'
        # Therefore an empty list would raise error when we want to extrct the first item i.e. getall()[0]
        try:
            p['pdf']     = 'https://arxiv.org' + response.xpath(pdf_xpath).getall()[0]
        except:
            pdf_xpath = '//a[text() = "PDF only"]/@href'
            p['pdf']     = 'https://arxiv.org' + response.xpath(pdf_xpath).getall()[0]
        
        yield p

    print("Memory usage in MB:",round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2))