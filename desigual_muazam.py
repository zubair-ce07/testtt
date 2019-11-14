from copy import deepcopy

from scrapy import Request
from scrapyproduct.spiderlib import SSBaseSpider

from scrapyproduct.items import ProductItem, SizeItem
from scrapyproduct.toolbox import (category_mini_item, extract_text_nodes)


class DesigualMuazam(SSBaseSpider):
    name = 'desigual_muazam'
    long_name = 'desigual muazam'
    base_url = 'https://www.desigual.com/en_US/'

    countries_info = [
        ('us', 'USD', 'en', 'https://www.desigual.com/en_US/', ['us']),
    ]

    country = ''
    max_stock_level = 1
    seen_identifiers = set()
    pagination_url_t = 'https://www.desigual.com/on/demandware.store/Sites-dsglcom_prod_us-Site/en_US/' \
                       'Search-UpdateGrid?{}&{}'

    def start_requests(self):
        for country_code, currency, language, country_url, same_region_dlrs in self.countries_info:
            if self.country and country_code not in self.country:
                continue
            meta = {
                'currency': currency,
                'cookiejar': country_code,
                'country_code': country_code,
                'language': language
            }

            yield Request(country_url, self.parse_homepage, meta=meta)

    def parse_homepage(self, response):
        for level1 in response.css('.nav-item.dropdown'):
            yield self.make_request(response, [level1])
            for level2 in level1.css('[class="dropdown-menu"] > li'):
                yield self.make_request(response, [level1, level2])
                for level3 in level2.css('.p-0 > li'):
                    yield self.make_request(response, [level1, level2, level3])

    def make_request(self, response, selectors):
        categories = [extract_text_nodes(sel.css('a'))[0] for sel in selectors]
        url = selectors[-1].css('a::attr(href)').extract_first()
        meta = deepcopy(response.meta)
        meta['categories'] = categories
        return Request(response.urljoin(url), self.parse_category, meta=meta, dont_filter=True)

    def parse_category(self, response):
        for product in response.css('.product'):
            identifier = product.css('::attr("data-pid")').extract_first()
            url = product.css('a::attr(href)').extract_first()
            item = ProductItem(
                url=response.urljoin(url),
                identifier=identifier,
                referer_url=response.url,
                category_names=response.meta['categories'],
                language_code=response.meta['language'],
                country_code=response.meta['country_code'],
                currency=response.meta['currency'],
                brand=self.long_name
            )
            yield category_mini_item(item)

            country_id = '{}_{}'.format(item['country_code'], item['identifier'])
            if country_id in self.seen_identifiers:
                continue

            self.seen_identifiers.add(country_id)
            meta = deepcopy(response.meta)
            meta['item'] = item
            yield Request(item['url'], self.parse_detail, meta=meta)

        for request in self.parse_pagination(response):
            yield request

    def parse_pagination(self, response):
        pages = response.css('noscript a::attr(href)').extract()
        cgid = response.css('.page::attr(data-querystring)').extract_first()
        for page in pages:
            query_param = page.split('?')[-1]
            next_url = self.pagination_url_t.format(cgid, query_param)
            yield Request(next_url, self.parse_category, meta=response.meta, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        item['title'] = response.css('.product-name::text').extract_first()
        item['base_sku'] = response.css('.product-id::text').extract_first()[:8]
        item['color_code'] = response.css('.product-id::text').extract_first()[-4:]
        item['description_text'] = extract_text_nodes(response.css('[data-gtm-label="product description"]'))
        item['image_urls'] = response.css('.primary-images img::attr(src)').extract()
        item['size_infos'] = self.get_size_infos(response)
        item['new_price_text'], item['old_price_text'] = self.get_prices(response)
        item['available'] = any(size['stock'] for size in item['size_infos'])

        return item

    def get_prices(self, response):
        price = response.css('.sales .value::attr(content)').extract_first()
        p_price = response.css('.strike-through.list .value::attr(content)').extract_first(price)
        return price, p_price

    def get_size_infos(self, response):
        size_infos = []
        sizes = response.css('.select-size')[0].css('option')[1:]
        for size in sizes:
            size_info = SizeItem(
                size_name=size.css('::attr(data-attr-value)').extract_first(),
                stock=1 if size.css('::attr(data-available)').extract_first() == 'true' else 0,
                size_identifier=size.css('::attr(data-attr-value)').extract_first()
            )
            size_infos.append(size_info)
        return size_infos
