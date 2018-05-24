# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
import canonicaljson
import hashlib

logger = logging.getLogger('pipelinelogger')

class BioschemasScraperPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        logger.info("Connected to MongoDB")
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        _id = hashlib.sha256(canonicaljson.encode_canonical_json(item['jsonld'])).hexdigest()
        self.collection.update({'_id':_id}, item['jsonld'], upsert=True)
        logger.info("Sample added to MongoDB database!")
        return item
