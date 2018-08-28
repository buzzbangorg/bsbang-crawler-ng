import datetime
import logging
from bioschemas_scraper.spiders.sitemap import urls
from bioschemas_scraper.custom import remove_url_schema, connect_db


class ScrapingMiddleware(object):

    def __init__(self, settings):
        self.client = connect_db(settings)
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

        self.already_crawled_urls = set()
        now = datetime.datetime.now()
        days = 7
        for doc in self.collection.find(projection={'url': True}):
            if now - doc['_id'].generation_time.replace(tzinfo=None) < datetime.timedelta(days=days):
                self.already_crawled_urls.add(doc['url'])

        logging.info('Got %d urls crawled within the last %d days', len(self.already_crawled_urls), days)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if request.url in self.already_crawled_urls:
            spider.logger.info(
                "URL already scraped in past 7 days - %s", request.url)
        else:
            spider.logger.debug("URL requested - %s", request.url)
            return None

    @staticmethod
    def process_response(request, response, spider):
        del request

        if response.status != 200:
            spider.logger.warn("Problem crawling page status - %s - %s", response.status, response.url)

        edited_url = remove_url_schema(response.url)
        if edited_url in urls:
            urls[edited_url] = 1
            spider.logger.info("Crawling %d of %d sitemap pages",
                               sum(urls.values()), len(urls))

        return response

    def process_exception(self, request, exception, spider):
        pass
