import os
import pymongo
import logging
import requests
import pandas as pd
from lxml import etree
from scrapy.conf import settings
from urllib.parse import urlsplit
from six.moves.configparser import ConfigParser
from scrapy.exceptions import CloseSpider


logger = logging.getLogger('custom-logger')


def remove_url_schema(url):
    split_url = urlsplit(url)
    edited_url = split_url.netloc + split_url.path + split_url.query + split_url.fragment
    return edited_url

def connect_db():
    client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            int(settings['MONGODB_PORT'])
        )
    try:
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise CloseSpider('Unable to connect to MongoDB')
    logger.info("Connected to MongoDB")
    return client

def drop_db(dbname):
    client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            int(settings['MONGODB_PORT'])
        )
    try:
        client.server_info()
        client.drop_database(dbname)
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise CloseSpider('Unable to connect to MongoDB')

def get_sitemap_url():
    config_file = "../config/settings.ini"
    parser = ConfigParser()
    parser.read(config_file)
    for section_name in parser.sections():
        if section_name == "Sitemaps":
            urls = list()
            for name, value in parser.items(section_name):
                urls.append(value)
                logger.info("Sitemap URL - %s", value)
            return urls
    raise CloseSpider('Sitemap URL not provided')

def parse_sitemap(sitemap_urls):
    urls = dict()
    for url in sitemap_urls:
        response = requests.get(url)
        sitemap_xml = etree.fromstring(response.content)
        for urlset in sitemap_xml:
            children = urlset.getchildren()
            edited_url = remove_url_schema(children[0].text)
            urls[edited_url] = 0
    return urls

def generate_report(stats):
    filepath = '../stats/scrapy_stats.csv' 
    
    stats['scraping time'] = stats['finish_time'] - stats['start_time']
    df = pd.DataFrame(list(stats.items()), columns=['parameter', 'value'])
    df.set_index('parameter', inplace=True)
    
    if not os.path.isfile(filepath):
        df.to_csv(filepath)
    else: 
        cdf = pd.read_csv(filepath, index_col='parameter')
        concat_df = pd.concat([df, cdf], axis=1, sort=False, join='inner')
        concat_df.to_csv(filepath)
