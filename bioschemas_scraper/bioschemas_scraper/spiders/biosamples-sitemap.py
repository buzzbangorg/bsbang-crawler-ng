import json
import scrapy
from scrapy.spiders import SitemapSpider
from extruct.jsonld import JsonLdExtractor  
from bioschemas_scraper.items import BioschemasScraperItem

class BiosamplesSitemapSpider(SitemapSpider):
    name = 'biosamples-sitemap'
    sitemap_urls = ['https://www.ebi.ac.uk/biosamples/sitemap']
    
    def parse(self, response):
        request = scrapy.Request(response.url, callback = self.parse_sample)
        yield request

    def parse_sample(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        item = BioschemasScraperItem()
        item['jsonld'] = jsonld
        yield item
