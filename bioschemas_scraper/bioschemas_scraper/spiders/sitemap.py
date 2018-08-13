import datetime
import logging
from extruct.jsonld import JsonLdExtractor
from bioschemas_scraper.custom import remove_url_schema, get_sitemap_url, parse_sitemap
from bioschemas_scraper.items import BioschemasScraperItem
from scrapy.spiders import SitemapSpider


logger = logging.getLogger('extract')


sitemap = get_sitemap_url()
urls = parse_sitemap(sitemap)


class BiosamplesSitemapSpider(SitemapSpider):
    name = 'sitemap'
    sitemap_urls = sitemap

    def parse(self, response):
        """
        @url http://www.ebi.ac.uk/biosamples/samples/SAMN04581192
        @returns items 1 1
        @returns requests 0 0
        @scrapes jsonld
        """
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        if len(jsonld) == 0:
            logger.warning("No bioschemas at this URL - %s", response.url)
            yield None
        else:
            item = BioschemasScraperItem()

            item['jsonld'] = {
                'schema': jsonld,
                'url': remove_url_schema(response.url),
                'datetime': datetime.datetime.utcnow().isoformat(),
                'crawler-id': 'buzzbang-ng'
            }

            logger.info("Sample Extracted - %s", response.url)
            yield item
