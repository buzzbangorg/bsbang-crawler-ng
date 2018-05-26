import pymongo
import logging
from scrapy.conf import settings
from urllib.parse import urlsplit


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

