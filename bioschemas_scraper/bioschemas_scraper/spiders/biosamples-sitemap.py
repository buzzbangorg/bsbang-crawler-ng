import json
import scrapy
import logging
from extruct.jsonld import JsonLdExtractor  
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bioschemas_scraper.items import BioschemasScraperItem

logger = logging.getLogger('sitemaplogger')

class BiosamplesSitemapSpider(SitemapSpider):
    name = 'biosamples-sitemap'
    # sitemap_urls = ['https://www.ebi.ac.uk/biosamples/sitemap']
    sitemap_urls = ['https://www.ebi.ac.uk/biosamples/sitemap']
    
    rules = (
    Rule(LinkExtractor(allow=('1/', ), ), callback='parse_crawl', follow=True),
  			)

    def parse(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        item = BioschemasScraperItem()
        item['jsonld'] = jsonld[0]
        logger.info("Sample Extracted - %s", response.url)
        yield item
