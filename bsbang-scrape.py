#!/usr/bin/env python3

import os
import argparse
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
settings = str()
for section_name in parser.sections():
    if section_name in allowed_settings_scrapy:
        setting = str()
        for name, value in parser.items(section_name):
            setting = setting + str('--set=') + \
                str(name) + '=' + str(value) + str(' ')
        settings = settings + setting


logfile = datetime.now().strftime("%Y%m%d-%H%M%S") + '-' + 'cronjob.log'
user_args = {
    'CONCURRENT_REQUESTS': args.con_req,
    'CONCURRENT_REQUESTS_PER_DOMAIN': args.con_req_dom,
}
for parameter, value in user_args.items():
    settings = settings + str('--set=') + \
        str(parameter) + '=' + str(value) + str(' ')
execute = "scrapy crawl " + settings + "sitemap"


if args.optimize is True:
    optimizer = {
        'OPTIMIZER_STATUS': True,
        'MONGODB_COLLECTION': 'test',
        'CLOSESPIDER_ITEMCOUNT': 200,
    }
    added_settings = settings
    for parameter, value in optimizer.items():
        added_settings = added_settings + \
            str('--set=') + str(parameter) + '=' + str(value) + str(' ')
    execute = "scrapy crawl " + added_settings + "sitemap"


if args.schedule is True:
    scheduler = {
        'LOG_FILE': '../log/' + logfile,
        'LOG_ENABLED': True,
    }
    added_settings = settings
    for parameter, value in scheduler.items():
        added_settings = added_settings + \
            str('--set=') + str(parameter) + '=' + str(value) + str(' ')
    execute = "scrapy crawl " + added_settings + "sitemap"

# print(execute)
path = 'cd ' + os.getcwd() + '/bioschemas_scraper '
os.system('bash bioschemas_scraper/scrape.sh ' +
          '"' + path + '" ' + '"' + execute + '"')
