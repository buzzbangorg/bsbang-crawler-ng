import scrapy
import logging
import requests
from lxml import etree
from scrapy.crawler import CrawlerProcess
from extruct.jsonld import JsonLdExtractor  
from scrapy.linkextractors import LinkExtractor
from bioschemas_scraper.items import BioschemasScraperItem
from scrapy.spiders import CrawlSpider, SitemapSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor


logger = logging.getLogger('sitemap-logger')

sitemap = "https://www.ebi.ac.uk/biosamples/sitemap"
urls = dict()

response = requests.get(sitemap)
sitemap_xml = etree.fromstring(response.content)
for urlset in sitemap_xml:
    children = urlset.getchildren()
    urls[children[0].text] = 0

class BiosamplesSitemapSpider(SitemapSpider):
    name = 'biosamples-sitemap'
    allowed_domains = ["ebi.ac.uk"]
    sitemap_urls = [sitemap]
    def parse(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        item = BioschemasScraperItem()
        item['jsonld'] = jsonld[0]
        logger.info("Sample Extracted - %s", response.url)
        yield item
