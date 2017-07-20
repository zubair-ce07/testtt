import json
import re

from scrapy import Spider

from training_spider.items import TrainingSpiderItem


class LemonSpider(Spider):
    name = 'lululemon'
    start_urls = [
        'http://shop.lululemon.com/'
    ]

    def parse(self, response):
        category_urls = response.css(
            '.section-nav[id]:not(:nth-child(7)) a::attr(href)'
        ).extract()

        for url in category_urls:
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response):
        products_urls = response.css('.prod-link::attr(href)').extract()

        for url in products_urls:
            yield response.follow(url, callback=self.parse_products)

    def parse_products(self, response):
        item = TrainingSpiderItem()
        item['product_id'] = response.css('#btn_add_to_bag::attr(data-productid)').extract_first()
        item['product_name'] = response.css('.original .OneLinkNoTx::text').extract_first()
        item['product_url'] = response.url
        item['country'] = 'USA'

        currency = response.css('.original .price-fixed::text').extract_first()
        item['currency'] = re.sub(r'[^A-Za-z]*', '', currency)

        variations = self.get_variations(response)
        item['variations'] = variations

        yield item

    def get_variations(self, response):
        raw_script = response.css('head script:not([src ])')

        sizes_keys = raw_script.re_first(r'sizeDriverString =  ({.*});')
        sizes_keys = json.loads(sizes_keys).keys()

        colors = raw_script.re_first(r'colorDriverString = ({.*});')
        colors = json.loads(colors)
        colors_keys = colors.keys()

        style_count = raw_script.re_first(r'styleCountDriverString = ({.*});')
        style_count = json.loads(style_count)

        variations = []
        for key in colors_keys:
            color = colors[key]
            sizes = self.get_sizes(color, sizes_keys)
            variation_key, main_images, image_urls = self.get_image_urls(
                response, style_count, key
            )

            variation_value = {
                'sizes': sizes,
                'image_url': image_urls,
                'main_images': main_images
            }

            variations.append({variation_key: variation_value})

        return variations

    def get_image_urls(self, response, style_count, color_key):
        image_urls = []
        main_images = []
        variation_key = ''
        for color in response.css('.color-swatch span[id]'):
            if color_key not in color.css('::attr(id)').extract_first():
                continue

            image = color.css('img')

            color_name = image.css('::attr(alt)').extract_first()
            variation_key = '{key}_{color_name}'.format(
                key=color_key,
                color_name=color_name
            )
            scene7url = image.css('::attr(data-scene7url)').extract_first()
            style_number = image.css('::attr(data-stylenumber)').extract_first()

            for number in range(int(style_count[style_number][0][0])):
                url = '{scene7url}{style_number}_{number}'.format(
                    scene7url=scene7url,
                    style_number=style_number,
                    number=number + 1
                )
                image_urls.append(url)
                if number < 2:
                    main_images.append(url)

        return variation_key, main_images, image_urls

    def get_sizes(self, color, sizes_keys):
        sizes = []
        available_sizes = []
        for size in color:
            _size = {
                'name': size[0],
                'price': size[2],
                'is_available': True
            }
            sizes.append(_size)
            available_sizes.append(size[0])

        for size_key in sizes_keys:
            if size_key in available_sizes:
                continue
            _size = {
                'name': size_key,
                'price': '-',
                'is_available': False
            }
            sizes.append(_size)

        return sizes
