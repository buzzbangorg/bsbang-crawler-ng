import logging

import psycopg2
import psycopg2.extras

from bioschemas_scraper.custom import connect_db


logger = logging.getLogger('mongodb')


class BioschemasScraperPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()

        o.client = connect_db(crawler.settings)
        # o.db = o.client[crawler.settings['MONGODB_DB']]
        # o.collection = o.db[crawler.settings['MONGODB_COLLECTION']]

        return o

    def process_item(self, item, spider):
        self.client.execute(
            'INSERT INTO crawl VALUES (%s, %s, %s, %s)',
            (item['url'], item['last_crawled'], item['crawler_id'], psycopg2.extras.Json(item['schema'])))

        # self.collection.insert_one(item['jsonld'])
        return item
