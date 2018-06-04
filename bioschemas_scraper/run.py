import io
from scrapy import cmdline
from six.moves.configparser import ConfigParser

config_file = "../config/settings.ini"
allowed_settings_scrapy = ['MongoDBServer', 'Logging', 'Concurrency Settings']
parser = ConfigParser()
parser.read(config_file)
settings = str()
for section_name in parser.sections():
    if section_name in allowed_settings_scrapy:
        setting = str()
        for name, value in  parser.items(section_name):
            setting = setting + str('--set=') + str(name) + '=' + str(value) + str(' ')
        settings = settings + setting

execute = "scrapy crawl " + settings +  "sitemap"
print(execute)
cmdline.execute(execute.split())
