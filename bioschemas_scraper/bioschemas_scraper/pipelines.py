# -*- coding: utf-8 -*-

import logging
from scrapy.conf import settings
from bioschemas_scraper.custom import connect_db


logger = logging.getLogger('mongodb')


class BioschemasScraperPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        client = connect_db()
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert_one(item['jsonld'])
        return item
