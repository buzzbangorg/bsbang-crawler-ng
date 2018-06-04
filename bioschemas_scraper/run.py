import io
import argparse
from scrapy import cmdline
from six.moves.configparser import ConfigParser

parser = argparse.ArgumentParser('If this is your first run on this hardware,'
                                  + ' you may consider optimizing performance with -o flag')

parser.add_argument('--optimize',
                    action='store_true',
                    help='If true then scraper will find optimal parameters')

args = parser.parse_args()


config_file = "../config/settings.ini"
allowed_settings_scrapy = ['MongoDBServer', 'Logging', 'Concurrency Settings']
parser = ConfigParser()
parser.optionxform = str
parser.read(config_file)
settings = str()
for section_name in parser.sections():
    if section_name in allowed_settings_scrapy:
        setting = str()
        for name, value in  parser.items(section_name):
            setting = setting + str('--set=') + str(name) + '=' + str(value) + str(' ')
        settings = settings + setting


execute = "scrapy crawl " + settings +  "sitemap"
print(execute)
cmdline.execute(execute.split())


# [Concurrency Settings]
# ;CONCURRENT_ITEMS=
# ;CONCURRENT_REQUESTS= 
# ;CONCURRENT_REQUESTS_PER_DOMAIN=
# ;CONCURRENT_REQUESTS_PER_IP=

