from math import ceil

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class CategoriesLinkExtractor(LinkExtractor):
    link_category_number_map = {
        'https://www.khelf.com.br/feminino-1.aspx/c': 1,
        'https://www.khelf.com.br/masculino-3.aspx/c': 3,
        'https://www.khelf.com.br/acessorios-4.aspx/c': 4
    }

    def _extract_links(self, response_text, response_url, response_encoding, base_url=None):
        links = []

        category = self.link_category_number_map.get(response_url)
        category_products_count = int(response_text.css('.filter-details strong:last-child::text').get())

        for page_number in range(1, ceil(int(category_products_count) / 21) + 1):
            link = (f'https://www.khelf.com.br/categoria/1/{category}/0//MaisRecente/Decrescente/21/{page_number}'
                    f'//0/0/.aspx')
            links.append(Link(link, '>'))

        return links
