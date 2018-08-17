import logging
from scrapy import signals
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured
from bioschemas_scraper.custom import connect_db, generate_report, drop_db


logger = logging.getLogger('statcol')


class StatsCollector(object):

    def __init__(self, stats):
        self.stats = stats
        self.initial_db_size = 0
        self.final_db_size = 0
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('EXT_ENABLED'):
            raise NotConfigured

        # instantiate the extension object
        ext = cls(crawler.stats)

        # connect the extension object to signals
        crawler.signals.connect(
            ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(
            ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        client = connect_db(crawler.settings)
        db = client[crawler.settings['MONGODB_DB']]
        ext.collection = db[crawler.settings['MONGODB_COLLECTION']]
        ext.item_count = crawler.settings['EXT_ITEMCOUNT']

        # return the extension object
        return ext

    def spider_opened(self, spider):
        self.initial_db_size = self.collection.count()
        logger.info("%d documents already present in the DB",
                    self.initial_db_size)
        logger.info("opened spider %s", spider.name)

    def spider_closed(self, spider):
        self.final_db_size = self.collection.count()
        logger.info("%d documents present in the DB after crawl",
                    self.final_db_size)
        logger.info("closed spider %s", spider.name)

        if bool(settings['OPTIMIZER_STATUS']) is True:
            drop_db(settings['MONGODB_DB'])

        final_stats = self.stats.get_stats().copy()
        final_stats['initial_db_size'] = self.initial_db_size
        final_stats['final_db_size'] = self.final_db_size
        final_stats['CONCURRENT_REQUESTS'] = settings['CONCURRENT_REQUESTS']
        final_stats['CONCURRENT_REQUESTS_PER_DOMAIN'] = settings[
            'CONCURRENT_REQUESTS_PER_DOMAIN']
        generate_report(final_stats)

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        if self.items_scraped % self.item_count == 0:
            logger.info("scraped %d items", self.items_scraped)
