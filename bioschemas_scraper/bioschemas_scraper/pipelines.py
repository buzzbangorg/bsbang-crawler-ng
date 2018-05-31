# -*- coding: utf-8 -*-

import hashlib
import canonicaljson
import logging
from scrapy.exceptions import DropItem
from bioschemas_scraper.custom import connect_db 


logger = logging.getLogger('mongodb')


class BioschemasScraperPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.collection = connect_db()

    def process_item(self, item, spider):
        _id = hashlib.sha256(canonicaljson.encode_canonical_json(item['jsonld'])).hexdigest()
        self.collection.update({'_id':_id}, item['jsonld'], upsert=True)
        logger.info("Sample added to MongoDB database!")
        return item
