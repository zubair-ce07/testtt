import logging
from urllib.parse import urlparse

import parsel


def find_urls_from_content(content, base_url):
    urls = set([])
    selector = parsel.Selector(text=content)
    for url in selector.css('a').xpath('@href').getall():
        if bool(urlparse(url).netloc):
            urls.add(url)
        else:
            urls.add(base_url + url)

    return urls


def get_logger(app_name):
    console_format = '[%(levelname)-5.5s]  %(message)s'
    log_format = '%(asctime)s [%(levelname)-5.5s]  %(message)s'

    logging.basicConfig(level=logging.INFO, format=console_format)

    logger = logging.getLogger(app_name)

    file_handler = logging.FileHandler('crawler.log')
    file_handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(file_handler)

    return logger
