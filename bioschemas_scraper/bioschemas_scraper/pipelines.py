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
        dbindex = self.collection.insert(item['jsonld'])
        if isinstance(self.collection.find_one({'_id': dbindex}), dict):
            logger.info("Sample added to MongoDB database!")
        else:
            logger.warning("Sample not added to MongoDB - %s", item['jsonld']['buzz_url'])
        return item
