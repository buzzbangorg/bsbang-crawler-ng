import scrapy
import logging
import requests
from lxml import etree
from extruct.jsonld import JsonLdExtractor  
from bioschemas_scraper.custom import remove_url_schema 
from bioschemas_scraper.items import BioschemasScraperItem
from scrapy.spiders import SitemapSpider


logger = logging.getLogger('extract')


sitemap = "https://www.ebi.ac.uk/biosamples/sitemap"
urls = dict()
response = requests.get(sitemap)
sitemap_xml = etree.fromstring(response.content)
for urlset in sitemap_xml:
    children = urlset.getchildren()
    edited_url = remove_url_schema(children[0].text)
    urls[edited_url] = 0


class BiosamplesSitemapSpider(SitemapSpider):
    name = 'sitemap'
    allowed_domains = ["ebi.ac.uk"]
    sitemap_urls = [sitemap]
    def parse(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        item = BioschemasScraperItem()
        item['jsonld'] = jsonld[0]
        logger.info("Sample Extracted - %s", response.url)
        yield item
        