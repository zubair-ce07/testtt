import json

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class ProductLinkExtractor(LinkExtractor):
    def _extract_links(self, response_text, response_url, response_encoding, base_url=None):
        raw_products = json.loads(response_text.response.body).get('results')[0]['hits']

        return [Link(f'https://www.journelle.com/products/{raw_product["named_tags"]["canonical"]}')
                for raw_product in raw_products]
