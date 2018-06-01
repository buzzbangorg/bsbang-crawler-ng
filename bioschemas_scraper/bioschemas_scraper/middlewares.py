# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from bioschemas_scraper.spiders.sitemap import urls
from bioschemas_scraper.custom import remove_url_schema
from bioschemas_scraper.custom import connect_db 


class ScrapingMiddleware(object):
    def __init__(self):
        self.collection = connect_db()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        x = self.collection.find_one({'buzz_url': remove_url_schema(request.url)})
        if x is not None:
            spider.logger.info("URL already scraped - %s", request.url)
            raise IgnoreRequest()
        else:
            spider.logger.info("URL requested - %s", request.url)
            return None

    def process_response(self, request, response, spider):
        spider.logger.info("Crawled - %s - %s", response.status, response.url)        
        edited_url = remove_url_schema(response.url)
        if edited_url in urls:
            urls[edited_url] = 1
            spider.logger.info("Crawling %d of %d pages", sum(urls.values()), len(urls))
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
