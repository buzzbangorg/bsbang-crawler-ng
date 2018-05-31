import logging
import requests
from lxml import etree
from extruct.jsonld import JsonLdExtractor  
from bioschemas_scraper.custom import remove_url_schema, get_domain, get_sitemap_url
from bioschemas_scraper.items import BioschemasScraperItem
from scrapy.spiders import SitemapSpider
from scrapy.exceptions import DropItem


logger = logging.getLogger('extract')


sitemap = get_sitemap_url()
urls = dict()
response = requests.get(sitemap)
sitemap_xml = etree.fromstring(response.content)
for urlset in sitemap_xml:
    children = urlset.getchildren()
    edited_url = remove_url_schema(children[0].text)
    urls[edited_url] = 0


class BiosamplesSitemapSpider(SitemapSpider):
    name = 'sitemap'
    allowed_domains = [get_domain(sitemap)]
    sitemap_urls = [sitemap]
    def parse(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        if len(jsonld) == 0:
            logger.warning("No bioschemas at this URL - %s", response.url)
            yield None
        else:
            item = BioschemasScraperItem()
            jsonld[0]['buzz_url'] = remove_url_schema(response.url)
            item['jsonld'] = jsonld[0]
            logger.info("Sample Extracted - %s", response.url)
            yield item
