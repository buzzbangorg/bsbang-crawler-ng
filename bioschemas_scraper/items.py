import scrapy


class BioschemasScraperItem(scrapy.Item):
    schema = scrapy.Field()
    url = scrapy.Field()
    last_crawled = scrapy.Field()
    crawler_id = scrapy.Field()
