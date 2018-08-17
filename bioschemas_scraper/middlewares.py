# -*- coding: utf-8 -*-
import datetime
from scrapy.conf import settings
from scrapy.spiders import SitemapSpider
from scrapy.exceptions import IgnoreRequest
from bioschemas_scraper.spiders.sitemap import urls
from bioschemas_scraper.custom import remove_url_schema, connect_db


class ScrapingMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()

        o.client = connect_db(crawler.settings)
        o.db = o.client[crawler.settings['MONGODB_DB']]
        o.collection = o.db[crawler.settings['MONGODB_COLLECTION']]

        return o

    def process_request(self, request, spider):
        x = self.collection.find_one(
            {'buzz_url': remove_url_schema(request.url)})
        if x is not None:
            if datetime.datetime.now() - x['_id'].generation_time.replace(tzinfo=None) < datetime.timedelta(days=7):
                spider.logger.info(
                    "URL already scraped in past 7 days - %s", request.url)
                raise IgnoreRequest()
            else:
                spider.logger.info("URL requested - %s", request.url)
                return None
        else:
            spider.logger.info("URL requested - %s", request.url)
            return None

    def process_response(self, request, response, spider):
        spider.logger.info("Crawled - %s - %s", response.status, response.url)
        edited_url = remove_url_schema(response.url)
        if edited_url in urls:
            urls[edited_url] = 1
            spider.logger.info("Crawling %d of %d pages",
                               sum(urls.values()), len(urls))
        return response

    def process_exception(self, request, exception, spider):
        pass
