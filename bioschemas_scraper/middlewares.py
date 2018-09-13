import logging
from bioschemas_scraper.spiders.sitemap import urls
from bioschemas_scraper.custom import remove_url_schema, connect_db

logger = logging.getLogger('statcol')


class ScrapingMiddleware(object):
    def __init__(self, settings):
        curs = connect_db(settings)
        days = 7
        self.already_crawled_urls = set()
        curs.execute("SELECT url FROM crawl WHERE last_crawled >= current_date - integer '%s'", (days,))
        for row in curs:
            self.already_crawled_urls.add(row[0])

        logger.info("Found %d URLs already scraped in the past %d days" % (curs.rowcount, days))

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
        if response.status != 200:
            spider.logger.warn("Problem crawling page status - %s - %s", response.status, response.url)

        edited_url = remove_url_schema(response.url)
        if edited_url in urls:
            urls[edited_url] = 1
            spider.logger.info("Crawling %d of %d sitemap pages",
                               sum(urls.values()), len(urls))

        return response
