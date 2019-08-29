import json

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class ProductLinkExtractor(LinkExtractor):
    def _extract_links(self, response_text, response_url, response_encoding, base_url=None):
        links = []

        products_data = json.loads(response_text.response.body).get('results')[0]['hits']
        for product_data in products_data:
            product_canonical = product_data["named_tags"]["canonical"]
            links.append(Link(f'https://www.journelle.com/products/{product_canonical}'))

        return links
