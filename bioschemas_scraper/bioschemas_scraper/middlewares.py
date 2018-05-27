from bioschemas_scraper.pipelines import collection
from bioschemas_scraper.spiders.sitemap import urls
from bioschemas_scraper.custom import remove_url_schema
from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware


class LogCrawlingMiddleware(BaseRedirectMiddleware):
    def process_request(self, request, spider):
        spider.logger.info("URL requested - %s", request.url)

    def process_response(self, request, response, spider):
        spider.logger.info("Crawled - %s - %s", response.status, response.url)        
        edited_url = remove_url_schema(response.url)
        if edited_url in urls:
            urls[edited_url] = 1
            spider.logger.info("Crawling %d of %d pages", sum(urls.values()), len(urls))
        return response

    def process_exception(self, request, exception, spider):
        pass
