from re import sub


from woolrich.items import WoolrichItem


class WoolrichParser:
    market = 'UK'
    currency = 'GBP'
    brand = 'woolrich'
    name = 'woolrichspider'
    retailer = 'woolrich-uk'
    genders = [
        ('women', 'women'),
        ('female', 'women'),
        ('lady', 'women'),
        ('woman', 'women'),
        ('man', 'men'),
        ('male', 'men'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('kids', 'unisex-kids'),
        ('adults', 'unisex-adults'),
    ]

    @classmethod
    def init_item(cls, response):
        item = WoolrichItem()
        item['url'] = response.url
        item['market'] = cls.market
        item['retailer'] = cls.retailer
        item['trail'] = response.meta['trail']
        item['name'] = cls.get_name(response)
        item['care'] = cls.get_care(response)
        item['image_urls'] = cls.get_image_urls(response)
        item['retailer_sku'] = cls.get_product_id(response)
        item['gender'] = cls.get_gender(response)
        item['description'] = cls.get_description(response)
        item['category'] = cls.get_categories(response)
        return item

    @staticmethod
    def add_trail(response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    @staticmethod
    def get_page_meta(response):
        css = '.search-result-content::attr({})'
        page_result = response.css(f'{css.format("data-pagesize")}, {css.format("data-searchcount")}').getall()
        return list(map(int, page_result))

    @staticmethod
    def get_in_stock(response):
        in_stock = response.css('.in-stock-msg::text').get()
        return int(sub(r'\sitem\sleft', '', in_stock)) if in_stock else 0

    @staticmethod
    def get_name(response):
        return response.css('#product-content .product-name::text').get().strip()

    @staticmethod
    def get_size_backlog(response):
        css = '.swatches.size .swatchanchor::{}'
        sizes = [s.strip() for s in response.css(css.format('text')).getall()]
        urls = response.css(css.format('attr(href)')).getall()
        return list(zip(urls, sizes))

    @staticmethod
    def get_colour_backlog(response):
        return response.css('.swatches.color .swatchanchor::attr(href)').getall()

    @staticmethod
    def get_product_id(response):
        return response.css('.sku::attr(skuid)').get().strip()

    @staticmethod
    def get_categories(response):
        return response.css('.breadcrumb-element::text').getall()[:-1]

    @staticmethod
    def get_description(response):
        descriptions = response.css('.description::text').getall()
        return [description.strip() for description in descriptions]

    @staticmethod
    def get_care(response):
        return [care.strip() for care in response.css('.fit-content::text').getall()]

    @staticmethod
    def get_image_urls(response):
        css = '#thumbnails .carousel-container-inner a::attr(href)'
        return response.css(css).getall()

    @classmethod
    def get_gender(cls, response):
        genders_candidate = ' '.join([response.url]
                                     + [url for title, url in response.meta['trail']]
                                     ).lower()
        for tag, gender in cls.genders:
            if tag in genders_candidate:
                return gender
        return 'unisex-adults'

    @classmethod
    def get_sku(cls, response, additional_attrs):
        colour_css = '.swatches.color .selected .swatch::text'
        price_css = '#product-content .price-sales::text'
        sku_item = {
            'currency': cls.currency,
            'colour': response.css(colour_css).get().strip(),
            'price': int(response.css(price_css).get()[1:].replace('.', '')),
            **additional_attrs
        }

        previous_prices = response.css('#product-content .price-sales::text').getall()
        if previous_prices:
            previous_prices = [int(p[1:].replace('.', '')) for p in previous_prices]
            sku_item['previous_prices'] = previous_prices

        sku_item['sku_id'] = cls.get_product_id(response)
        sku_item['in_stock'] = cls.get_in_stock(response)
        return sku_item
