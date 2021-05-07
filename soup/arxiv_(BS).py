import time # For measuring the elapsed time
from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import itertools # For chaining/flattening the urls list from different catagories of CS into one list
import os
import psutil # For memory usage

limit = True # Setting the limit boolean 
url = 'https://arxiv.org' # Starting webpage
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')
tags = bs.find_all('a', {'id':re.compile("^cs\..*")})

#Using regex to find the values for href
a = re.findall('href="(.*?)"',str(tags))
print("Links of categories in computer science recent papers...")
target_link = []
for link in a:
    target_link.append('https://arxiv.org'+link)
print(target_link)
print("Printing information for each paper...")

# Extracting the url for CS papers in all catagories. This part will be will be measure by time function
start = time.time()
ht = []
for i in range(len(target_link)):
	html = request.urlopen(target_link[i])
	bs = BS(html.read(), 'html.parser')
	tags = bs.find_all('a',{'title':re.compile("Abstract")})
	ht.append(re.findall('\/abs.*?\.\d+',str(tags)))
	if limit:
		# Since every category yields a list of papers, therefore ht would be a list of lists. To flatten 
		# the list and make the urls into one list, we used chain function from itertools 
		if len(list(itertools.chain(*ht))) > 100:
			paper_url = ['https://arxiv.org' + i for i in list(itertools.chain(*ht))][0:100]			
	else:
		paper_url = ['https://arxiv.org' + i for i in list(itertools.chain(*ht))]

# Scraping the information from gathered links for papers
d = pd.DataFrame({'Title':[], 'Category': [], 'Authors':[],'Date':[], 'PDF':[]})

for link in paper_url:
	html = request.urlopen(link)
	bs = BS(html.read(), 'html.parser')
	Title = bs.find('h1',{"class": "title mathjax"}).text[6:]
	if '[cs.' in bs.find('td',{"class":"tablecell arxivid"}).text:
		Category = bs.find('td',{"class":"tablecell arxivid"}).text[-3:-1]
	else: # To make sure that it gets the CS tags if the paper is an interdisciplinary
		temp = bs.find('td',{"class":"tablecell subjects"}).text
		Category = re.findall('\(cs.[A-Z].+?\)',temp)[0][-3:-1]
	Authors = bs.find('div',{"class": "authors"}).text[8:]
	Date = bs.find('div',{"class":"dateline"}).text.strip()[14:25].split(']')[0]
	PDF = link.replace('abs','pdf')
	paper = {'Title':Title,'Category':Category,'Authors':Authors,'Date':Date,'PDF':PDF}
	print(paper)
	d = d.append(paper, ignore_index = True)

# Stoping the stopwatch
end = time.time()
print(d)
print("Elapsed time during scraping in seconds:",round(end - start,2)) 
print("Memory usage in MB:",round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2))
# Output to csv file
d.to_csv('papers.csv',index=False)