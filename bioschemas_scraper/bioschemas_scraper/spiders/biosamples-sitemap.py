import json
import scrapy
import logging
from scrapy.spiders import SitemapSpider
from extruct.jsonld import JsonLdExtractor  
from bioschemas_scraper.items import BioschemasScraperItem

logger = logging.getLogger('sitemaplogger')

class BiosamplesSitemapSpider(SitemapSpider):
    name = 'biosamples-sitemap'
    sitemap_urls = ['https://www.ebi.ac.uk/biosamples/sitemap']
    
    def parse(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        item = BioschemasScraperItem()
        item['jsonld'] = jsonld
        logger.info("Sample Extracted - %s", response.url)
        yield item
