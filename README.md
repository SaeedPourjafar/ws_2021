## Instruction for running the scrapers

<b>Beautiful Soup</b>: For running the Beautiful Soup scraper, from your CMD/Terminal please go to the directory in which the `arxiv_(BS).py` is located and then run the file by using either:

``` bash
# For linux
python3 arxiv_(BS).py
# For Windows
python arxiv_(BS).py
```
Alternatively you can run the file from your text editor. In Sublime3 you can press Ctrl+B to run the codes (for the first time you may want to press Ctrl+Shift+B to declare your preferd python interpreter if you have more than one version of python)

<b>Scrapy</b>: For runing the spiders first put all the files (`arxiv1.py`,`arxiv2.py`,`arxiv3.py`) into the spiders folder and then from your CMD/Terminal navigate to the scrapy project folder. Please run the commands below in this particular order:<br>
```
scrapy crawl topics -o topics.csv
scrapy crawl computer -o computer.csv
scrapy crawl papers -o papers.csv
```
<b>Selenium</b>: For running the Selenium scraper, first open the `arxiv_(Selenium).py` file and change the custom path of the webdriver so it can find the executable file for your browser's driver (either Chrome webdriver or Geckodriver for Firefox). Save the file and then from the your CMD/Terminal locate the file and run the command below:<br>

```bash
# For linux
python3 arxiv_(Selenium).py
# For Windows
python arxiv_(Selenium).py
```
Alternatively you can run the file from your text editor as described above.

