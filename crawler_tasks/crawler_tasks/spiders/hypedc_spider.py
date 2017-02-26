from itertools import product

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler_tasks.items import HypedcProduct


class HypedcSpider(CrawlSpider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = ['https://www.hypedc.com/']
    rules = (
        Rule(LinkExtractor(allow=('\.html',)), callback='parse_product'),
        Rule(LinkExtractor(allow=('\w+/mens/', '\w+/womens/', '\w+/kids/')), follow=True),
    )

    def parse_product(self, response):
        parent = response.css('section header div#carousel-product')
        form = parent.css('form#product_addtocart_form')

        item = HypedcProduct()
        item['url'] = response.url
        item['product_id'] = form.css('input[name=product]::attr(value)').extract_first()
        item['name'] = form.css('h1.product-name::text').extract_first()
        item['brand'] = form.css('h2.product-manufacturer::text').extract_first()
        item['market'] = ''
        item['merch_info'] = []
        item['category'] = response.css('section ul.breadcrumb li[class^="category"] a::attr(title)').extract()
        item['care'] = form.css('div.product-description[itemprop=description] ul li::text').extract()
        item['gender'] = item['category'][0]
        item['image_urls'] = parent.css('div#main-image li:not(li.clone) img::attr(data-src)').extract()
        item['description'] = form.css('div.product-description[itemprop=description]::text').extract_first()

        price_container = form.css('div.product-price-container')
        price = price_container.css('meta[itemprop=price]::attr(content)').extract_first()
        currency = price_container.css('meta[itemprop=priceCurrency]::attr(content)').extract_first()
        available_colours = self.__get_available_colours(response, form)
        available_sizes = self.__get_available_sizes(form)

        item['skus'] = self.__create_skus(available_colours, available_sizes, currency, price)
        return item

    def __get_available_colours(self, response, form):
        current_colour = form.css('.product-colour::text').extract()
        other_colours = response.css('div#carousel-colours .product-name::text').extract()
        return other_colours + current_colour

    def __get_available_sizes(self, parent):
        size_option_container = parent.css('div#product-options-wrapper')
        size_scales = size_option_container.css('ul#size-selector-desktop-tabs li:not(li.tab-label)')
        sizes_per_scale_container = size_option_container.css('div#size-selector-desktop-content')

        scale_names = size_scales.css('a::text').extract()
        sizes_per_scale_div_ids = size_scales.css('a::attr(href)').extract()
        scale_names_and_sizes_div_ids = zip([x.replace(' ', '') for x in scale_names],
                                            [x.lstrip('#') for x in sizes_per_scale_div_ids])
        available_sizes = []
        for scale_name, sizes_div_id in scale_names_and_sizes_div_ids:
            scale_sizes = sizes_per_scale_container.css(
                'div#{} li[data-stock=in] a::text'.format(sizes_div_id)).extract()
            available_sizes.extend(['{}-{}'.format(scale_name, size) for size in scale_sizes])

        return available_sizes

    def __create_skus(self, colours, sizes, currency, price):
        skus = {}
        color_size_combinations = product(colours, sizes)
        for colour, size in color_size_combinations:
            skus['{}_{}'.format(colour, size)] = {'color': colour, 'size': size, 'currency': currency, 'price': price}
        return skus
