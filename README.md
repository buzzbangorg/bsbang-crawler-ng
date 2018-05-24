# bsbang-crawler-ng
Repository for the next generation Scrapy based Buzzbang Bioschemas crawler

Schema.org is a collaborative effort to bring semantic markup to the web. This project provides web developers with schemas to represent a range of different objects in their websites. Search engines can extract useful information from websites without having to dig into the HTML structure of all the websites they crawl.     

Schema.org defines common generic types like events and datasets which can be used not just in life sciences but in many other disciplines. Bioschemas is working on specifications to improve the description of generic types in life sciences.

Buzzbang is an alpha project to start crawling this data so that it can then be searched in the companion frontend project. 

## Getting Started
Create a virtual environment and clone this repo, before installing the dependencies
```
virtualenv buzzbang
source buzzbang/bin/activate
git clone https://github.com/buzzbangorg/bsbang-crawler-ng.git
cd bsbang-crawler-ng
pip install -r requirements.txt
```

## Usage
Step 1: Crawl the relevant website using a sitemap and store the data in a mongoDB daabase
```
cd bioschemas_scraper
python run.py
```

## Running the tests
TBD

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the Apache-2.0 License - see the LICENSE file for details
