import scrapy
import json

from extruct.jsonld import JsonLdExtractor  


class BiosamplesSpider(scrapy.Spider):
    name = "biosamples"
    allowed_domains = ['ebi.ac.uk']
    start_urls = ['https://www.ebi.ac.uk/biosamples/samples?start=0',]

    def parse(self, response):
        # for _id in response.xpath("//span[@class='lead float-left text-left']").extract():
        #     yield {'sample_id' : _id}

        base = 'https://www.ebi.ac.uk'
        urls = response.xpath("//a[@class='button readmore float-right']/@href").extract()
        for url in urls:
            request = scrapy.Request(base + url, callback = self.parse_sample)
            yield request

        # process next page
        next_page_url = response.xpath("//li[@class='pagination-next']//a/@href").extract_first()
        if next_page_url is not None:
            request = scrapy.Request(next_page_url, callback = self.parse)
            yield request


    def parse_sample(self, response):
        jslde = JsonLdExtractor()
        jsonld = jslde.extract(response.body)
        yield {'JSONLD' : jsonld}
        