import scrapy
import bs4
import json
import requests

from extruct.jsonld import JsonLdExtractor  


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)
            return r
    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        return self.build_response_from_file(request)

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
        # jsonld = self.extract_jsonld_from_url(response.request.url)
        yield {'JSONLD' : jsonld}

    def extract_jsonld_from_url(self, url):
        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())
        r = requests_session.get(url)
        return r.text
