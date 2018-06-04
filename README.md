# bsbang-crawler-ng
Repository for the next generation Scrapy based Buzzbang Bioschemas crawler

**THIS IS NOT YET COMPLETE, PLEASE DO NOT USE YET**

Schema.org is a collaborative effort to bring semantic markup to the web. This project provides web developers with schemas to represent a range of different objects in their websites. Search engines can extract useful information from websites without having to dig into the HTML structure of all the websites they crawl.     

Schema.org defines common generic types like events and datasets which can be used not just in life sciences but in many other disciplines. Bioschemas is working on specifications to improve the description of generic types in life sciences.

Buzzbang is an alpha project to start crawling this data so that it can then be searched in the companion frontend project. 

## Getting Started
**Step 1: Create a virtual environment and clone this repo**

```
pip3 install virtualenv
python3 -m virtualenv buzzbang
source buzzbang/bin/activate
git clone https://github.com/buzzbangorg/bsbang-crawler-ng.git
cd bsbang-crawler-ng
```

**Step 2: Install Python dependencies**

```
pip3 install -r requirements.txt
```

**Step 3: Install MongoDB if necessary**

You may follow this [blog](https://hevodata.com/blog/install-mongodb-on-ubuntu/) to install MongoDB on your system. 


Setup the MongoDB server using MongoDBServer settings in the conf/settings.ini file.
Start and check if the MongoDB server is up using the following commands in another terminal - 
```
service mongodb start
service mongodb status
``` 

## Usage
**Step 1: Put initialization arguments in the config/setting.ini file**

**Step 2: Crawl the sitemap of the website and store the data in a MongoDB database**

```
cd bioschemas_scraper
python3 run.py
```

The scrapy stats is logged in stats/scrapy_stats.csv file. Please use this for deciding proper initializations.

TODO: Implementation and documentation of inserting this data into Solr.

## Running the tests
TBD

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the Apache-2.0 License - see the LICENSE file for details


## Scrapy Implementations

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
- [ ] Allow scrapy to crawl multiple domains/sitemaps 
- [ ] Hardware benchmarking for optimal performance across various machines 
- [ ] Handle unsuccessful responses - 40X and keep track of those URLs   
- [ ] Check the faithfulness of JSON-LD - if it is from Life Sciences domain
- [ ] ........ if you have more suggestions, let's discuss at the issues section
