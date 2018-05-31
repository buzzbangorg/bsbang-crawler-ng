import pymongo
import logging
from scrapy.conf import settings
from urllib.parse import urlsplit
from six.moves.configparser import ConfigParser
from scrapy.exceptions import CloseSpider

logger = logging.getLogger('custom-logger')


def remove_url_schema(url):
    split_url = urlsplit(url)
    edited_url = split_url.netloc + split_url.path + split_url.query + split_url.fragment
    return edited_url

def connect_db():
    client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
    logger.info("Connected to MongoDB")
    db = client[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]
    return collection

def get_domain(url):
    split_url = urlsplit(url)
    return split_url.netloc
    
def get_sitemap_url():
    config_file = "../config/settings.ini"
    parser = ConfigParser()
    parser.read(config_file)
    for section_name in parser.sections():
        if section_name == "Sitemaps":
            for name, value in  parser.items(section_name):
                if name == "sitemap":
                    print(value)
                    return value
    logger.error("Sitemap URL not provided")
    raise CloseSpider()
