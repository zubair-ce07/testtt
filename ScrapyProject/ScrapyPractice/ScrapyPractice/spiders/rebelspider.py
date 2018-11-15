import scrapy

from scrapy import Request
from urllib.parse import urljoin, urlparse

from ScrapyPractice.items import ProductItem
from ScrapyPractice.items import SizeItem
from ScrapyPractice.items import VariationItem


class MangoSpider(scrapy.Spider):
    name = "rebelspider"
    domain_url = "https://www.rebelsport.com.au"

    def start_requests(self):
        start_url = 'https://www.rebelsport.com.au/brands'
        yield Request(start_url, callback=self.parse)

    def parse(self, response):
        brands_list_xpath = "//div[@id='secondary']//ul[@id='category-level-1']/li/a/@href"
        brand_urls = response.xpath(brands_list_xpath).extract()

        for url in brand_urls[0:1]:
            yield Request(
                url=url,
                callback=self.parse_brand
            )

    def parse_brand(self, response):
        product_xpath = "//ul[@id='search-result-items']/li/div/div[1]/a[1]/@href"
        next_page_xpath = "//div[@data-loading-state='unloaded']/@data-grid-url"

        product_urls = response.xpath(product_xpath).extract()
        for url in product_urls:
            req_url = urljoin(self.domain_url, url)
            yield Request(
                url=req_url,
                callback=self.parse_product,
            )

        next_page_url = response.xpath(next_page_xpath).extract_first(default=None)
        if next_page_url:
            yield Request(
                url=next_page_url,
                callback=self.parse_brand
            )

    def parse_product(self, response):
        des_xpath = "//div[@id='product-description']//p/text() | //div[@id='product-description']//ul/li/text()"
        product = ProductItem(
            product_url=response.xpath("//span[@itemprop='url']/text()").extract_first().strip(),
            title=response.xpath("//h1[@class='product-name']/text()").extract_first(),  # .strip(),
            brand=response.xpath("//span[@class='product-brand']/text()").extract_first(),
            locale="en_AU",
            currency="AUD",
            variations=[],
            breadcrumbs=response.xpath("//*[@class='breadcrumb-element']/text()").extract(),
            description=response.xpath(des_xpath).extract(),
        )
        product["store_keeping_unit"] = product['product_url'].split('-')[-1].split('.')[0]

        colors_exist = response.xpath("//div[@class='product-variations']").extract()
        if not colors_exist:
            yield self.parse_no_variation_items(response, product)
            return

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

            product['variations'][-1]['sizes'].append(
                SizeItem(
                    size_name=size_name,
                    is_available=True,
                    price=price_dict['price'],
                    is_discounted=price_dict['is_discounted'],
                    discounted_price=price_dict['discounted_price'],
                )
            )

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
                sizes=SizeItem(
                    size_name=None,
                    is_available=True,
                    price=price_dict['price'],
                    is_discounted=price_dict['is_discounted'],
                    discounted_price=price_dict['discounted_price'],
                ),
            )
        )

        return product

    def parse_no_size_item(self, response, product):
        price_dict = self.get_price_values(response)

        product['variations'][-1]['sizes'].append(
            SizeItem(
                size_name=None,
                is_available=True,
                price=price_dict['price'],
                is_discounted=price_dict['is_discounted'],
                discounted_price=price_dict['discounted_price'],
            )
        )
        path = "//li[contains(@class,'selected')]/following-sibling::li[not(contains(@class,'unselectable'))]/a/@href"
        next_color = response.xpath(path).extract_first()
        if next_color:
            return Request(
                url=next_color,
                callback=self.color_info,
                meta={'product': product},
            )

        return product

    def get_price_values(self, response):
        price_standard = response.xpath("//span[@class='price-standard']/text()").extract_first(default=None)
        price_sales = response.xpath("//span[@class='price-sales']/text()[2]").extract_first().strip()

        if "N/A" in price_sales:
            return {
                'is_discounted': False,
                'price': None,
                'discounted_price': '',
            }

        price_sales= price_sales.split('$')[1]

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
