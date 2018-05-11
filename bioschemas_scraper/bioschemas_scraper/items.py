# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BioschemasScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sample_id = scrapy.Field()
    sample_key = scrapy.Field()
    pass
