import copy

from scrapy import Request, Spider, signals
from urllib.parse import urljoin
from ScrapyPractice.items import ProductItem, SizeItem, VariationItem


class RebelSpider(Spider):
    name = "rebelspider"
    domain_url = "https://www.rebelsport.com.au"
    items = dict()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(RebelSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.process_items, signal=signals.spider_idle)
        return spider

    def process_items(self, spider):
        while self.items:
            sku, item = self.items.popitem()
            req = Request(
                url=urljoin(self.domain_url, item['product_url']),
                callback=self.parse_product,
                meta={'item': item},
            )
            self.crawler.engine.crawl(req, self)

    def start_requests(self):
        start_url = 'https://www.rebelsport.com.au'
        yield Request(start_url, callback=self.parse_homepage)

    def parse_homepage(self, response):
        for category_level1 in response.xpath("//nav[@id='navigation']/ul/li")[0:1]:
            yield self.make_request([category_level1], response)

            for category_level2 in category_level1.xpath(".//div[@class='level-2-outer']")[0:1]:
                yield self.make_request([category_level1, category_level2], response)

                for category_level3 in category_level2.xpath(".//div/ul/li")[0:10]:
                    yield self.make_request([category_level1, category_level2, category_level3], response)

    def make_request(self, selectors, response):
        category_level1_label = [sel.xpath("./a/text()").extract_first('').strip() for sel in selectors]
        url = selectors[-1].xpath("./a/@href").extract_first()
        meta = copy.deepcopy(response.meta)
        meta['category'] = category_level1_label
        return Request(
            url=url,
            callback=self.parse_categories,
            meta=meta,
        )

    def parse_categories(self, response):
        for product in response.xpath("//ul[@id='search-result-items']/li"):
            item = ProductItem(breadcrumbs=[])
            item['product_url'] = product.xpath(".//div[@class='product-image']/a/@href").extract_first()
            item['store_keeping_unit'] = product.xpath("./div/@data-itemid").extract_first()
            item['breadcrumbs'].append(response.meta['category'])

            if item['store_keeping_unit'] not in self.items.keys():
                self.items[item['store_keeping_unit']] = item
            else:
                self.items[item['store_keeping_unit']]['breadcrumbs'].append(item['breadcrumbs'])

        next_page_xpath = "//div[@class='search-result-content']/div[@data-loading-state='unloaded']/@data-grid-url"
        next_page = response.xpath(next_page_xpath).extract_first()

        # if next_page:
        #     yield Request(
        #         url=next_page,
        #         callback=self.parse_categories,
        #         meta=response.meta,
        #     )
        # pass

    def parse_product(self, response):
        item = response.meta['item']

        des_xpath = "//div[@id='product-description']//p/text() | //div[@id='product-description']//ul/li/text()"
        product = ProductItem(
            product_url=response.url,
            title=response.xpath("//h1[@class='product-name']/text()").extract_first(),
            brand=response.xpath("//span[@class='product-brand']/text()").extract_first(),
            locale="en_AU",
            currency="AUD",
            variations=[],
            breadcrumbs=item['breadcrumbs'],
            description=response.xpath(des_xpath).extract(),
        )
        product["store_keeping_unit"] = item["store_keeping_unit"]

        color_xpath = "//ul[@class='swiper-wrapper swatches color']/li[not(contains(@class,'unselectable'))][1]/a/@href"
        color_url = response.xpath(color_xpath).extract_first()
        if color_url:
            yield Request(
                url=color_url,
                callback=self.color_info,
                meta={'product': product}
            )
            return
        yield self.parse_no_variation_items(response, product)

    def color_info(self, response):
        product = response.meta['product']

        color_name = response.xpath("//li[contains(@class,'selected')]/a/img/@alt").extract_first()
        images = response.xpath("//div[@id='pdp-swiper']/div[1]//a/@href").extract()
        if color_name:
            product['variations'].append(
                VariationItem(
                    display_color_name=color_name,
                    images_urls=images,
                    sizes=[],
                )
            )

            size_url = response.xpath("//option[@data-lgimg][1]/@value").extract_first()
            if not size_url:
                yield self.parse_no_size_item(response, product)
                return

            yield Request(
                url=size_url,
                callback=self.size_info,
                meta={'product': product}
            )

    def size_info(self, response):
        product = response.meta['product']
        size_name = response.xpath("//option[@selected]/text()").extract_first()

        if size_name:
            size_name = size_name.strip()
            price_dict = self.get_price_values(response)

            product['variations'][-1]['sizes'].append(self.make_size_item(size_name, price_dict))

            next_size_url = response.xpath("//option[@selected]/following-sibling::option[1]/@value").extract_first()
        else:
            next_size_url = response.xpath("//option[@data-lgimg][1]/@value").extract_first()

        if next_size_url:
            yield Request(
                url=next_size_url,
                callback=self.size_info,
                meta={'product': product},
            )
            return

        path = "//li[contains(@class,'selected')]/following-sibling::li[not(contains(@class,'unselectable'))]/a/@href"
        next_color = response.xpath(path).extract_first()
        if next_color:
            yield Request(
                url=next_color,
                callback=self.color_info,
                meta={'product': product},
            )
            return

        yield product

    def parse_no_variation_items(self, response, product):
        price_dict = self.get_price_values(response)

        product['variations'].append(
            VariationItem(
                display_color_name=None,
                images_urls=response.xpath("//div[@id='pdp-swiper']/div[1]//a/@href").extract(),
                sizes=self.make_size_item(None, price_dict),
            )
        )

        return product

    def parse_no_size_item(self, response, product):
        price_dict = self.get_price_values(response)

        product['variations'][-1]['sizes'].append(self.make_size_item(None, price_dict))
        path = "//li[contains(@class,'selected')]/following-sibling::li[not(contains(@class,'unselectable'))]/a/@href"
        next_color = response.xpath(path).extract_first()
        if next_color:
            return Request(
                url=next_color,
                callback=self.color_info,
                meta={'product': product},
            )

        return product

    def make_size_item(self, size_name, price):
        return SizeItem(
            size_name=size_name,
            is_available=True,
            price=price['price'],
            is_discounted=price['is_discounted'],
            discounted_price=price['discounted_price'],
        )

    def get_price_values(self, response):
        price_standard = response.xpath("//span[@class='price-standard']/text()").extract_first(default=None)
        price_sales = response.xpath("//span[@class='price-sales']/text()[2]").extract_first().strip()

        if "N/A" in price_sales:
            return {
                'is_discounted': False,
                'price': None,
                'discounted_price': '',
            }

        price_sales = price_sales.split('$')[1]

        if price_standard and "N/A" not in price_standard:
            is_discounted = True
            price = float(price_standard.strip().split('$')[1].replace(',', ''))
            discounted_price = float(price_sales.replace(',', ''))
        else:
            is_discounted = False
            price = float(price_sales.replace(',', ''))
            discounted_price = ''

        return {
            'is_discounted': is_discounted,
            'price': price,
            'discounted_price': discounted_price,
        }
