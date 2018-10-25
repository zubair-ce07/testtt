# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from json import loads

from scrapy import FormRequest, Request, Spider
from scrapy.selector import Selector

from scrapy_advance_training.items import ProductItem, SizeInfosItem


class NeimanmarcusSpider(Spider):
    name = 'neimanmarcus'
    allowed_domains = ['neimanmarcus.com']
    start_urls = ['https://www.neimanmarcus.com/']

    pagination_service_url = 'https://www.neimanmarcus.com/en-pk/category.service'
    size_color_service_url = 'https://www.neimanmarcus.com/en-pk/product.service'
    navigation_service_url = 'https://www.neimanmarcus.com/en-pk/deferred.service'
    navigation_params = '{"RWD.deferredContent.DeferredContentReqObj":{"contentPath":' \
                        '"/page_rwd/header/silos/silos.jsp","category":"cat000000"}}'
    pagination_params = '{{"GenericSearchReq":{{"pageOffset":{},"pageSize":{},"definitionPath"' \
                        ':"/nm/commerce/pagedef_rwd/template/EndecaDrivenHome","rwd":"true",' \
                        '"categoryId":{}}}}}'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    color_id_re = re.compile('_\w+_')
    category_id_re = re.compile('cat[0-9]+')

    def parse(self, response):
        params = {'data': self.navigation_params}
        yield FormRequest(self.navigation_service_url, self.parse_navigation, formdata=params)

    def parse_navigation(self, response):
        nav_info = loads(response.text)
        selector = Selector(text=nav_info['RWD.deferredContent.DeferredContentRespObj']['content'])
        designer_url = selector.css('.all a::attr(href)').extract_first()
        yield Request(designer_url, self.parse_designers)

        for navigation_url in selector.css('a::attr(href)').extract():
                yield Request(response.urljoin(navigation_url), self.parse_products)

    def parse_designers(self, response):
        for category_url in response.css('a[itemprop="significantLink"]::attr(href)').extract():
            yield Request(response.urljoin(category_url), self.parse_products)

    def parse_products(self, response):
        if not response.meta.get('pagination_done'):
            category_names = response.css('.bcClick a::text').extract()
            if not category_names:
                return

            for product_url in response.css('#productTemplateId::attr(href)').extract():
                yield Request(response.urljoin(product_url), self.parse_product,
                              meta={'cat_names': category_names})
            yield from self.request_pagination(response, category_names)
        else:
            products = loads(response.text)
            selector = Selector(text=products['GenericSearchResp']['productResults'])
            for url in selector.css('#productTemplateId::attr(href)').extract():
                yield Request(response.urljoin(url),
                              self.parse_product,
                              meta={'cat_names': response.meta['cat_names']})

    def request_pagination(self, response, category_names):
        page_size = response.css('.productsPerPage::text').extract_first()
        total_pages = response.css('#epagingTop .pageOffset')

        if not total_pages:
            return

        total_pages = int(total_pages[-1].css('::attr(pagenum)').extract_first('0'))
        category_id = re.findall(self.category_id_re, response.url)[0]
        for page_offset in range(total_pages):
            params = {
                'data': self.pagination_params.format(page_offset, page_size, category_id),
                'service': 'getCategoryGrid'
            }
            yield FormRequest(self.pagination_service_url,
                              self.parse_products,
                              formdata=params,
                              meta={'pagination_done': True, 'cat_names': category_names})

    def parse_product(self, response):
        availability_msg = response.css('.cannotorder::text').extract()

        if availability_msg:
            return

        product_item = ProductItem(
            url=response.url,
            category_names=response.meta['cat_names'],
            referer_url=response.request.headers.get('Referer', ''),
            language_code=response.css('html::attr(lang)').extract_first(),
            country_code=response.css('.intl-countrycode::attr(value)').extract_first(),
            currency=response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first(),
        )

        for product in response.css('.hero-zoom-frame'):
            yield self.parse_variation(product, deepcopy(product_item))
        else:
            yield self.parse_variation(response, product_item)

    def parse_variation(self, product, product_item):
        availability_msg = product.css('.error-text::text').extract_first()
        if availability_msg:
            return

        old_price, new_price = self.extract_price(product)

        identifier = product.css('div[itemprop="offers"]::attr(product_id)').extract_first()

        product_item['identifier'] = identifier
        product_item['new_price_text'] = new_price
        product_item['old_price_text'] = old_price
        product_item['full_price_text'] = new_price
        product_item['title'] = product.css('span[itemprop="name"]::text').extract_first()
        product_item['description_text'] = product.css('.productCutline li::text').extract()
        product_item['brand'] = product.css('span[itemprop="brand"] a::text').extract_first()

        image_urls = product.css('.alt-img-wrap img::attr(src)').extract()
        params = {
            'data': '{"ProductSizeAndColor":{"productIds":' + identifier + '}}'
        }
        return FormRequest(self.size_color_service_url,
                           self.parse_size_color,
                           formdata=params,
                           meta={'item': product_item, 'image_urls': image_urls})

    def parse_size_color(self, response):
        product_item = response.meta['item']
        image_urls = response.meta['image_urls']

        size_color_infos = loads(response.text)
        size_color_infos = loads(size_color_infos['ProductSizeAndColor']['productSizeAndColorJSON'])
        color_info = dict()
        for size_color_info in size_color_infos[0]['skus']:
            size_item = SizeInfosItem(
                size_identifier=size_color_info['sku'],
                size_name=size_color_info.get('size', 'one size'),
                stock=1 if size_color_info['stockAvailable'] else 0
            )
            self.extract_color_info(size_color_info, color_info, size_item)

        for color, item in color_info.items():
            product_itm = deepcopy(product_item)

            product_itm['available'] = 'true'
            product_itm['color_name'] = color
            product_itm['base_sku'] = item[1]
            product_itm['color_code'] = item[0]
            product_itm['size_infos'] = item[2:]
            product_itm['sku'] = item[1] + item[0]
            product_itm['image_urls'] = self.get_image_urls(item[0], image_urls, response)
            yield product_itm

    def get_image_urls(self, color_id, image_urls, response):
        new_image_urls = list()
        for image_url in image_urls:
            if 'scene7' in image_url and color_id not in image_url:
                image_url = re.sub(self.color_id_re, '_{}_'.format(color_id), image_url)
                new_image_urls.append(response.urljoin(image_url))
            else:
                new_image_urls.append(response.urljoin(image_url))
        return new_image_urls

    @staticmethod
    def extract_color_info(color, color_info, size_item):
        base_sku = color['cmosSku'][:-5]
        color_id = color['cmosSku'][-5:-3]
        color_name = color.get('color', 'one color').replace('?null?false', '')
        color_info.setdefault(color_name, [color_id, base_sku])
        color_info[color_name].append(size_item)

    @staticmethod
    def extract_price(response):
        new_price = response.css('p[itemprop="price"]::text').extract_first('').strip()
        old_price = ''
        if not new_price:
            price = response.css('.item-price::text').extract()[:2]
            return [p.strip() for p in price]

        return old_price, new_price
