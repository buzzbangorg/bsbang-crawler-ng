#!/usr/bin/env python3

import argparse
import bioschemas_scraper.settings
import bioschemas_scraper.spiders.sitemap as sitemap
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from datetime import datetime
from six.moves.configparser import ConfigParser


parser = argparse.ArgumentParser('If this is your first run on this hardware,'
                                 + ' you may consider optimizing performance')
parser.add_argument('-con_req',
                    nargs='?',
                    type=int,
                    default=8,
                    help='Input parameter CONCURRENT_REQUESTS, def: 8')
parser.add_argument('-con_req_dom',
                    nargs='?',
                    type=int,
                    default=100,
                    help='Input parameter CONCURRENT_REQUESTS_PER_DOMAIN, def: 100')
parser.add_argument('--optimize',
                    action='store_true',
                    help='If true then scraper will find optimal parameters')
parser.add_argument('--schedule',
                    action='store_true',
                    help='Used by scheduler, please don\'t use this flag')
args = parser.parse_args()


config_file = "config/settings.ini"
allowed_settings_scrapy = ['MongoDBServer', 'Logging', 'Concurrency Settings']
parser = ConfigParser()
parser.optionxform = str
parser.read(config_file)
overiding_settings = {}

for section_name in parser.sections():
    if section_name in allowed_settings_scrapy:
        for name, value in parser.items(section_name):
            overiding_settings[name] = value


logfile = datetime.now().strftime("%Y%m%d-%H%M%S") + '-' + 'cronjob.log'
user_args = {
    'CONCURRENT_REQUESTS': args.con_req,
    'CONCURRENT_REQUESTS_PER_DOMAIN': args.con_req_dom,
}

if args.optimize is True:
    optimizer = {
        'OPTIMIZER_STATUS': True,
        'MONGODB_COLLECTION': 'test',
        'CLOSESPIDER_ITEMCOUNT': 200,
    }

if args.schedule is True:
    scheduler = {
        'LOG_FILE': '../log/' + logfile,
        'LOG_ENABLED': True,
    }


settings = Settings()
settings.setmodule(bioschemas_scraper.settings)
settings.update(overiding_settings)

p = CrawlerProcess(settings=settings)

spider = sitemap.BiosamplesSitemapSpider()
spider.custom_settings = overiding_settings
p.crawl(spider)
p.start()
