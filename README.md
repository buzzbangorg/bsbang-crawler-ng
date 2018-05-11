# bsbang-crawler-ng
Repository for the next generation Scrapy based Buzzbang Bioschemas crawler


Instructions to run - 

```
cd bioschemas_scraper
scrapy crawl biosamples -o items.csv -t csv
```

The extracted json-ld is temporarily stored in items.csv file. 