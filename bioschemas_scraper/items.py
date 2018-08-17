# -*- coding: utf-8 -*-

import scrapy


class BioschemasScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jsonld = scrapy.Field()
