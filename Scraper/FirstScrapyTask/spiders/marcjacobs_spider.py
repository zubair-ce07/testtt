import re
import json
import urllib.parse

from scrapy import Request, Spider
from slugify import slugify

from FirstScrapyTask.items import MarcJacobsItem


class MarkJacobsSpider(Spider):
    ignore_links = ['GIFTS', 'NEW ARRIVALS', 'SALE']
    locale_t = 'en_{}'
    size_price_api_t = 'https://www.marcjacobs.com/on/demandware.store/Sites-marcjacobs-Site' \
                       '/default/Product-Variation?pid={0}&dwvar_{0}_color={1}&dwvar_{0}_size={2}'
    base_url = 'https://www.marcjacobs.com/'
    name = 'marc_jacobs'
    start_urls = ['https://www.marcjacobs.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        for parent_category in response.css('.mobile-hidden'):
            parent = parent_category.css('a::attr(title)').extract_first()
            if parent in self.ignore_links:
                continue
            for child_category in parent_category.css('.level-2 .menu-vertical >li'):
                child_url = child_category.css('a::attr(href)').extract_first()
                child = child_category.css('a::text').extract_first()
                if child_url:
                    yield self.product_urls_request(child_url, [parent,child])
                for grand_child_category in child_category.css('.level-3 >li'):
                    grand_child_url = grand_child_category.css('a::attr(href)').extract_first()
                    grand_child = grand_child_category.css('a::text').extract_first()
                    if grand_child_url:
                        yield self.product_urls_request(grand_child_url, [parent,child,grand_child])

    def product_urls_request(self, url, category_labels):
        product_category = '/'.join(label.strip().lower() for label in category_labels)
        meta = {'product_category': product_category}
        return Request(url=url, callback=self.parse_product_urls, meta=meta)

    def parse_product_urls(self, response):
        product_urls = self.remove_duplication(response.css('.product-page-link::attr(href)').extract())
        for url in product_urls:
            url = urllib.parse.urljoin(self.base_url, url)
            yield Request(url=url, callback=self.parse_product, meta=response.meta)
        pagination_api = response.css('.infinite-scroll-placeholder::attr(data-grid-url)').extract_first()
        if pagination_api:
            yield Request(url=pagination_api, callback=self.parse, meta=response.meta)

    def remove_duplication(self, products_urls):
        name_type_product = set()
        final_product_urls = []
        for url in products_urls:
            name = re.search('.+/', url).group(0)
            type = re.search('\?.+=', url).group(0)
            if name in name_type_product and type in name_type_product:
                continue
            else:
                final_product_urls.append(url)
                name_type_product.add(name)
                name_type_product.add(type)
        return final_product_urls

    def get_description(self , response):
        description = response.css('.pdp-detail-list li::text').extract()
        description.append(response.css('.product-details-copy::text').extract_first().strip())
        return description

    def parse_product(self, response):
        product = MarcJacobsItem()
        product['product_url'] = response.url
        product['product_id'] = response.css('.product-number span::text').extract_first()[1:]
        product['title'] = response.css('.product-name::text').extract_first()
        product['category'] = response.meta['product_category']
        product['description'] = self.get_description(response)
        product['locale'] = self.locale_t.format(response.css('.current-country span::text').extract_first())
        product['currency'] = response.css('script').re_first('currency: \'(.+)\'')
        product['variations'] = {}

        colors_urls = response.css('.attribute li a::attr(href)').extract()
        images_api = response.css('.product-images::attr(data-images)').re_first('.+')
        colors = response.css('.value .swatches.Color a::text').extract()
        color_codes = response.css('.value .swatches.Color a::attr(style)').re('background: url\(\/\/.+/.+_(.+)_+')
        sizes = response.css('.variation-select option::text').extract()[1:]
        color_images_urls = [re.sub('_(\d{3})_', '_{}_'.format(code), images_api) for code in color_codes]
        images_api = color_images_urls.pop()
        code_images_size = {}
        for code in  color_codes:
            code_images_size[code] = {'code': code,'image_urls': [], 'sizes': []}
        meta = {
            'product': product,
            'color_codes': color_codes,
            'colors': colors,
            'sizes': sizes,
            'color_images_urls': color_images_urls,
            'code_images_size': code_images_size,
            'color_urls': colors_urls,
        }
        yield Request(url=images_api, callback=self.parse_images_urls, meta=meta)

    def parse_images_urls(self , response):
        images_json = json.loads(re.search('app.mjiProduct.handleJSON\((.+)\);', response.text).group(1))
        color_code = re.search('_(\d{3})_',response.url).group(1)
        response.meta['code_images_size'][color_code]['image_urls'] = \
            [image_paths['src'] for image_paths in images_json['items']]
        if response.meta['color_images_urls']:
            yield Request(
                url=response.meta['color_images_urls'].pop(),
                callback=self.parse_images_urls,
                meta=response.meta
            )
        else:
            yield Request(
                url=response.meta['color_urls'].pop(),
                callback=self.parse_color_sizes,
                meta=response.meta,
                dont_filter=True
            )

    def parse_color_sizes(self , response):
        color_code = re.search('color=(\d{3})', response.url).group(1)
        available_sizes = response.css('.variation-select option::text').extract()[1:]
        response.meta['code_images_size'][color_code]['sizes'] = available_sizes
        if response.meta['color_urls']:
            yield Request(url=response.meta['color_urls'].pop(), callback=self.parse_color_sizes, meta=response.meta)
        else:
            sizes_urls = self.get_size_urls(response.meta['code_images_size'], response.meta['product']['product_id'])
            product_size_url = sizes_urls.pop()
            for color_code in response.meta['code_images_size']:
                response.meta['code_images_size'][color_code]['sizes'] = []
            response.meta['sizes_urls'] = sizes_urls
            yield Request(url=product_size_url, callback=self.parse_sizes_info, meta=response.meta, dont_filter=True)

    def parse_sizes_info(self , response):
        color_code = re.search('color=(.+)&', response.url).group(1)
        size = response.css('input#size::attr(value)').extract_first()
        response.meta['code_images_size'][color_code]['sizes'].append(self.create_size_item(response, size))
        if response.meta['sizes_urls']:
            yield Request(
                url=response.meta['sizes_urls'].pop(),
                callback=self.parse_sizes_info,
                meta=response.meta,
                dont_filter=True
            )
        else:
            colors = response.meta['colors']
            for index, code in enumerate(response.meta['color_codes']):
                response.meta['product']['variations'][slugify(colors[index])] = response.meta['code_images_size'][code]
            yield response.meta['product']

    def get_size_urls(self, code_images_size , product_code):
        colors_sizes_urls = []
        for code in code_images_size:
            for size in code_images_size[code]['sizes']:
                colors_sizes_urls.append(self.size_price_api_t.format(product_code, code, size.strip()))
        return colors_sizes_urls

    def create_size_item(self , response , size):
        is_available = response.css('.input-text::attr(data-available)').extract_first()
        standard_price = response.css('.quickview-tab .price-standard::text').extract_first()
        sales_price = response.css('.quickview-tab .price-sales::text').extract_first().strip()
        return {
            'size_name': size,
            'is_available': bool(int(is_available)),
            'is_discounted': bool(standard_price),
            'price': standard_price or sales_price,
            'discounted_price': sales_price if standard_price else ''
        }

