from selenium import webdriver
import time
import os
import psutil # For memory usage
import re
import pandas as pd # For dataframe output
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# For not explicitly wait for elements to load
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
capabilities = DesiredCapabilities.FIREFOX      
limit = True # Setting the limit to 100 pages

# Custom path to geckodriver
gecko_path = 'C:\\uw\\DSBA 2\\Web Scraping\\bonus\\geckodriver.exe'

url = 'https://arxiv.org' # Starting webpage

options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options = options, executable_path = gecko_path)
wait = WebDriverWait(driver, 30) # Maximum wait time
# Actual program:
start = time.time()
driver.get(url)
# Clicking the "Advanced Search" button when it appears
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/header/div[2]/div[2]/form/div/div[1]/p/a[2]'))) 
driver.execute_script("window.stop();")
button = driver.find_element_by_xpath('/html/body/div/header/div[2]/div[2]/form/div/div[1]/p/a[2]')
button.click()

# Clicking the checkbox for "Computer Science" when it appears
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div/form/section[2]/fieldset[1]/div[2]/div[1]/div[1]/div/div/input'))) 
button = driver.find_element_by_xpath('/html/body/main/div[2]/div[2]/div[1]/div/form/section[2]/fieldset[1]/div[2]/div[1]/div[1]/div/div/input')
button.click()

# Clickig the "Search" button when it appears
button = driver.find_element_by_xpath('/html/body/main/div[2]/div[2]/div[1]/div/form/section[3]/button')
button.click()
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/nav[1]/a[2]'))) 


# Initializing the empty list for informations of papers
Title_list = []
Category_list = []
A_list = []
Date_list = []
PDF_list = []

# Function to scrape required info for each paper
def scrape(driver):
	# We wait for the last title to be load, instead of explicitly waiting for the whole page to load
	# This is beneficial since it's more efficient
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/ol/li[50]/p[1]'))) 
	# To scrape the title using regex
	title = re.findall(r'<p class="title is-5 mathjax">([\s\S]*?)<\/p>', driver.page_source)
	for t in title:
		Title_list.append(t.strip())

	# We wait for the last category to be visible
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/ol/li[50]/div/div/span[1]')))
	# To scrape the category
	category = driver.find_elements_by_class_name("tags.is-inline-block")
	for c in category:
		if 'cs.' in c.text: # To make sure that it gets the CS tags if the paper is an interdisciplinary
			Category_list.append(re.findall('cs.[A-Z][A-Z]',c.text)[0][-2:])
		else:
			print("None")
	
	# Again we wait for the author of the last paper to be load
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/ol/li[50]/p[2]')))
	# To scrape the authors by using the class name
	Authors = driver.find_elements_by_class_name("authors")
	for a in Authors:
		A_list.append(a.text[9:]) # To remove "Authors: " from the beginning of the string

	# Waiting for the date of the last paper to be load
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/ol/li[50]/p[4]'))) 
	# To scrape the submitted date by using regex 
	date = re.findall(r'<span class="has-text-black-bis has-text-weight-semibold">Submitted<\/span> ([\s\S]*?)[^;]+<\/p>', driver.page_source)
	for d in date:
		Date_list.append(d[:-1])

	# Waiting for the pdf link of the last paper to be load
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/ol/li[50]/div/p/span/a[1]')))
	# To scrape the PDF url by using regex
	PDF = re.findall(r'https:\/\/arxiv.org\/pdf\/[^"]+', driver.page_source)
	for p in PDF:
		PDF_list.append(p)
	
	# To click the "Next" button after achieving the required data in each page
	wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/nav[1]/a[2]'))) 
	driver.find_element_by_xpath('/html/body/main/div[2]/nav[1]/a[2]').click()


if limit:
	for i in range(2): # For 100 papers, since in each page we have 50 results
		scrape(driver)
# Assuming around 800 papers to scrape when the limit is set to fasle. In total there are more 
# than 327360 pages in recent CS papers
else:
	for i in range(16): # For 800 papers, since in each page we have 50 results
		scrape(driver)
end = time.time()
print("Elapsed time during scraping in seconds:",round(end - start,2)) 
print("Memory usage in MB:",round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2,2))

# Saving to dataframe and output as CSV file
t = pd.Series(Title_list, name = 'Title')
c = pd.Series(Category_list, name = 'Category')
a = pd.Series(A_list, name = 'Authors')
d = pd.Series(Date_list, name = 'Date')
p = pd.Series(PDF_list, name = 'PDF')
df = pd.concat([t,c,a,d,p], axis=1)

df.to_csv('papers.csv', index=False)

driver.quit()