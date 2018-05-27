# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import hashlib
import canonicaljson
from bioschemas_scraper.custom import connect_db 
from scrapy.exceptions import DropItem


logger = logging.getLogger('mongodb')

collection = connect_db()

class BioschemasScraperPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.collection = collection

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        _id = hashlib.sha256(canonicaljson.encode_canonical_json(item['jsonld'])).hexdigest()
        self.collection.update({'_id':_id}, item['jsonld'], upsert=True)
        logger.info("Sample added to MongoDB database!")
        return item
