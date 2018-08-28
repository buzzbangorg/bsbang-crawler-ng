# bsbang-crawler-ng
Repository for the next generation Scrapy based Buzzbang Bioschemas crawler

Schema.org is a collaborative effort to bring semantic markup to the web. This project provides web developers with schemas to represent a range of different objects in their websites. Search engines can extract useful information from websites without having to dig into the HTML structure of all the websites they crawl.     

Schema.org defines common generic types like events and datasets which can be used not just in life sciences but in many other disciplines. Bioschemas is working on specifications to improve the description of generic types in life sciences. The community is very actively working to develop new schemas and the biobanks and related communities are following their schema to markup the data. You may see the live deploys here - [BioSchemas Live Deploys](https://github.com/BioSchemas/bioschemas.github.io/blob/master/_liveDeploys/liveDeploy.md)

Buzzbang is an alpha project to start crawling this data so that it can then be searched in the companion frontend project. 

## Getting Started
**Step 1: Create a virtual environment and clone this repo**

```
pip3 install virtualenv
python3 -m venv buzzbang-venv
source buzzbang-venv/bin/activate
git clone https://github.com/buzzbangorg/bsbang-crawler-ng.git
cd bsbang-crawler-ng
```

**Step 2: Install Python dependencies**

```
pip3 install -r requirements.txt
```

**Step 3: Install MongoDB if necessary**

Install MongoDB on your system.

Setup the MongoDB server using MongoDBServer settings in the conf/settings.ini file.

Start and check if the MongoDB server is up using the following commands in another terminal - 
```
service mongodb start
service mongodb status
``` 

## Usage
**Step 1: Copy config/settings.ini.example to settings.ini and configure**

The defaults are probably going to be fine but you might want to check them with the optimization procedure as explained later on.

**Step 2: Find optimal value of parameters for your hardware**

There are two parameters that you need to tune for faster crawling on your system - 'CONCURRENT_REQUESTS' - [4,8,16,32] and 'CONCURRENT_REQUESTS_PER_DOMAIN' - [100,500,1000]. Put different values of these parameters and view the stats report in log/scrapy_stats.csv file. For benchmarking, we are scraping 200 items (fixed) from the sitemap and we observe the 'scraping time' in the stats file for each pair of these two parameters. The pair that minimizes this time is best for your system.

Note: If you observe that increasing 'CONCURRENT_REQUESTS' is making your scraper faster, do not go about wildly increasing it. Check if the 'memusage/max' is less than or equal to 80% of CPU capacity. Beyond this, your system will choke.

```
./scrape.py -con_req <No. of concurrent requests> -con_req_dom <No. of concurrent request/domain> --optimize
```

**Step 3: Crawl the sitemap and store the data in a MongoDB database**

Supply the tuned parameters and run the script.

```
./scrape.py -con_req <No. of concurrent requests> -con_req_dom <No. of concurrent request/domain>
```

**Step 4: Schedule the crawler to recrawl the sitemaps at reqular intervals**

This step is only required if you want the crawler to run at regular intervals.

```
./schedule.py -con_req <No, of concurrent requests> -con_req_dom <No. of concurrent request/domain> -freq <No. of days after which to repeat> -py_path=<path to python interpreter in your virtuaenv>
```

eg:

```
./schedule.py -con_req 8 -con_req_dom 100 -freq 3 -py_path /home/innovationchef/Desktop/buzzbang/bin/python3
```

One may check the cronjob with ```crontab -l``` and check the last execution status using ```service cron status```

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the Apache-2.0 License - see the LICENSE file for details


## Mind Map
- [x] Sitemap Crawling
- [x] JSON-LD Extraction
- [x] Item Pipeline Implementation
- [x] MongoDB Connection
- [x] Logging number of pages already crawled - [i of n] 
- [x] Logging number of items already scraped 
- [x] Separate extension for logging stats
- [x] Generate reports in spreadsheet for performance comparison
- [x] Log request and response status
- [x] Prevent scraping items that are already scraped and kept in MongoDB
- [x] Raise exceptions for DB conn error & sitemap url error
- [x] Allowed user settings outside source control
- [x] Unittests - Spider contracts 
- [x] Filter out malicious massive input webpages, 
- [x] Hardware benchmarking for optimal performance across various machines 
- [x] Allow scrapy to crawl multiple domains/sitemaps 
- [x] Record the scraping time in DB as well
- [x] Write a Job scheduler for scheduling crawls
- [x] Recrawl URLs which were crawled more than 7 days ago
- [x] Error Checking in MongoDB using getLastError
- [ ] Check the faithfulness of JSON-LD - if it is from Life Sciences domain - To be skipped
- [ ] Handle unsuccessful responses - 40X and keep track of those URLs   
- [ ] Write general scraper for pagination - issue 18
- [ ] Make logging quieter
- [ ] Create a common format for MongoDB database for different crawlers - decide on which metadata to store  
