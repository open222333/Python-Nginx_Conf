from configparser import ConfigParser
import logging
import json


config = ConfigParser()
config.read('config/config.ini')

logger = logging.getLogger('nginx_config')



NGINX_DIR = config.get('BASIC', 'NGINX_DIR', fallback='')
with open('config/ns_list.json', 'r') as f:
    NS_LIST = json.load(f)
