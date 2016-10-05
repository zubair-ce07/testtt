import scrapy
from scrapy.http import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from veromada_spider.items import VeromadaSpiderItem


class VeromodaScrapper(CrawlSpider):
    name = "veromoda"
    allowed_domains = ["veromoda.com"]
    start_urls = ["http://www.veromoda.com/gb/en/"]

    rules = [
        Rule(LinkExtractor(restrict_css='li.category-navigation__item > section > ul > li'),),
        Rule(LinkExtractor(restrict_css='.product-tile__name'),
             callback='parse_product')
    ]

    def parse(self, response):
        garment = VeromadaSpiderItem()
        garment['spider_name'] = self.name
        garment['currency'] = 'GBP',
        garment['market'] = 'UK'
        garment['brand'] = 'VeroModa'
        garment['name'] = self.garment_name(response)
        garment['description'] = self.garment_description(response)
        garment['care'] = self.garment_care(response)
        garment['price'] = self.garment_price(response)
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['image_urls'] = self.garment_image_urls(response)
        garment['gender'] = 'women'
        garment['category'] = self.garment_category(response)
        garment['skus'] = {}
        color_urls = self.get_color_urls(response)
        return self.next_color_requests(color_urls, garment)

    def next_color_requests(self, color_urls, garment):
        if color_urls:
            link = color_urls.pop()
            yield scrapy.Request(url=link, callback=self.parse_next_color_sku, method='GET',
                                 headers={"Accept": "text/html, */*; q=0.01",
                                          "Accept-Encoding": "gzip, deflate, sdch",
                                          "X-Requested-With": "XMLHttpRequest"
                                        },
                                 meta={'garment': garment, 'color_urls': color_urls}
            )
        else:
            yield garment

    def parse_next_color_sku(self, response):
        garment = response.meta["garment"]
        color_urls = response.meta["color_urls"]
        lengths = response.css('ul.swatch.length li > a').extract()

        if not lengths:
            garment['skus'].update(self.product_skus(response))
            return self.next_color_requests(color_urls, garment)
        else:
            garment['image_urls'].append(self.garment_image_urls(response))
            selectable_sizes_x = 'ul.swatch.size li[class*=item--selectable] > a::attr(data-href)'
            selectable_sizes_urls = response.css(selectable_sizes_x).extract()
            selectable_sizes_request_urls = [url + '&Quantity=1&format=ajax' for url in selectable_sizes_urls]
            return self.size_request(selectable_sizes_request_urls, garment, color_urls)

    def size_request(self, selectable_sizes_request_urls, garment, color_urls):
        if selectable_sizes_request_urls:
            link = selectable_sizes_request_urls.pop()
            return scrapy.Request(link, method='GET',
                                  headers={"Accept": "text/html, */*; q=0.01",
                                           "Accept-Encoding": "gzip, deflate, sdch",
                                           "X-RequestedWith": "XMLHttpRequest"
                                  },
                                  callback=self.garment_size_detailed_sku,
                                  meta={'garment': garment, 'selectable_size_requests': selectable_sizes_request_urls,
                                        'color_urls': color_urls}
            )
        else:
            return self.next_color_requests(color_urls, garment)

    def garment_size_detailed_sku(self, response):
        garment = response.meta['garment']
        color = response.css('p.color-combination::text').extract_first()
        selectable_size_requests = response.meta['selectable_size_requests']
        color_urls = response.meta['color_urls']
        selected_size = response.css('ul.swatch.size li[class*=item--selected] > a::text').extract_first()
        selectable_lengths_css = 'ul.swatch.length li[class*=item--selectable] > a::text'
        unselectable_lengths_css = 'ul.swatch.length li[class*=item--unselectable] > a::text'
        unselectable_lengths = self.clean(response.css(unselectable_lengths_css).extract())
        selectable_lengths = self.clean(response.css(selectable_lengths_css).extract())
        sku_elements = self.get_static_sku_elements(response)
        lengths = selectable_lengths + unselectable_lengths

        for length in lengths:
            if color:
                if length in selectable_lengths:
                    sku_details = sku_elements.copy()
                    sku_details['size'] = selected_size.strip()
                    sku_details['out_of_stock'] = False
                    sku_details['color'] = color
                    sku_details['length'] = length
                    sku_key = color + '_' + selected_size.strip() + '_' + length
                    garment['skus'][sku_key] = sku_details
                else:
                    sku_details = sku_elements.copy()
                    sku_details['size'] = selected_size.strip()
                    sku_details['out_of_stock'] = True
                    sku_details['color'] = color
                    sku_details['length'] = length
                    sku_key = color + '_' + selected_size.strip() + '_' + length
                    garment['skus'][sku_key] = sku_details

        return self.size_request(selectable_size_requests, garment, color_urls)

    def product_skus(self, response):
        product_skus = {}
        color = response.css('p.color-combination::text').extract_first()
        unselectable_sizes = response.css('ul.swatch.size li[class*=unselectable] > a::text').extract()
        selectable_sizes = response.css('ul.swatch.size li[class*=item--selectable] > a::text').extract()
        sku_elements = self.get_static_sku_elements(response)
        sizes = selectable_sizes + unselectable_sizes

        if not color:
            pass
        else:
            for size in sizes:
                if size in selectable_sizes:
                    sku_details = sku_elements
                    sku_details['size'] = size.strip()
                    sku_details['color'] = color
                    sku_details['out_of_stock'] = False
                    sku_key = color + '_' + sku_details['size']
                    product_skus[sku_key] = sku_details
                else:
                    sku_details = sku_elements
                    sku_details['size'] = size.strip()
                    sku_details['color'] = color
                    sku_details['out_of_stock'] = True
                    sku_key = color + '_' + sku_details['size']
                    product_skus[sku_key] = sku_details

        return product_skus

    def garment_name(self, response):
        return response.css('section[class=product-info]>h1[class*=product-name]::text').extract_first()

    def garment_description(self, response):
        description = response.css('div[class*=pdp-description__text]::text').extract()
        return self.clean(description)

    def garment_care(self, response):
        care_cautions = response.css('ul[class=pdp-description__list]>li::text').extract()
        return self.clean(care_cautions)

    def garment_price(self, response):
        return response.css('.value__price::text').extract_first()

    def garment_image_urls(self, response):
        return response.css('li[class=product-images__main__image]>img::attr(src)').extract()

    def garment_category(self, response):
        return response.css('div[class=breadcrumb] a::attr(title)').extract()

    def clean(self, item_list):
        return [item.strip() for item in item_list if not item.isspace()]

    def get_color_urls(self, response):
        colours_css = response.css("ul.swatch.colorpattern li > a::attr(data-href)").extract()
        colour_urls = [url + '&Quantity=1&format=ajax' for url in colours_css]
        colour_urls.append(''.join([response.url, '&Quantity=1&format=ajax']))
        return colour_urls

    def get_static_sku_elements(self, response):
        return {'price': self.garment_price(response), 'currency': 'GBP'}

