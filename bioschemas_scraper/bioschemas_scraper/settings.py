# -*- coding: utf-8 -*-

SPIDER_MODULES = ['bioschemas_scraper.spiders']
NEWSPIDER_MODULE = 'bioschemas_scraper.spiders'

ITEM_PIPELINES = {'bioschemas_scraper.pipelines.MongoDBPipeline': 300}

#### MongoDB Settings
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "ebi_biosamples"
MONGODB_COLLECTION = "samples"

#### Crawl responsibly by identifying yourself (and your website) on the user-agent
ROBOTSTXT_OBEY = True
BOT_NAME = 'bioschemas_scraper'
USER_AGENT = 'Buzzbang Project (https://github.com/buzzbangorg)'

#### Log setting Block
LOG_LEVEL = 'INFO' 			#   'CRITICAL' > 'ERROR' > 'WARNING' > 'INFO' > 'DEBUG'
# LOG_FILE = 'log/log'
# LOG_ENABLED = True

#### Disable Cookies
COOKIES_ENABLED = False
RETRY_ENABLED = True 

#### Autothrottle Setting Block
AUTOTHROTTLE_ENABLED = True 
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 20.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 40.0 
AUTOTHROTTLE_DEBUG = False  # Enable it only if you want to see the live status
# DOWNLOAD_DELAY = 

#### Concurrency Settings - To be tested
# CONCURRENT_ITEMS = 
# CONCURRENT_REQUESTS = 
# CONCURRENT_REQUESTS_PER_DOMAIN = 
# CONCURRENT_REQUESTS_PER_IP = 

# SPIDER_MIDDLEWARES = {
#    'bioschemas_scraper.middlewares.BioschemasScraperSpiderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
   'bioschemas_scraper.middlewares.BioschemasScraperDownloaderMiddleware': 543,
}

#### Cache Setting - Do not enable it until you are debugging the code
#HTTPCACHE_ENABLED = True 
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
