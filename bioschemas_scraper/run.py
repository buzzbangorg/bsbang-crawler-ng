import io
from scrapy import cmdline
from six.moves.configparser import ConfigParser

config_file = "../config/settings.ini"
parser = ConfigParser()
parser.read(config_file)
settings = str()
for section_name in parser.sections():
    # print('Section:', section_name)
    # print('  Options:', parser.options(section_name))
    # for name, value in parser.items(section_name):
    #     print('  {} = {}'.format(name, value))
    setting = str()
    for name, value in  parser.items(section_name):
        setting = setting + str('--set=') + str(name) + '=' + str(value) + str(' ')
    
    settings = settings + setting

execute = "scrapy crawl " + settings +  "sitemap"
cmdline.execute(execute.split())
