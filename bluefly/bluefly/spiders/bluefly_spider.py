from bluefly.items import BlueflyItem
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class BlueflySpiderSpider(CrawlSpider):
    name = "bluefly_spider"
    allowed_domains = ["bluefly.com"]
    start_urls = [
        'http://www.bluefly.com',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=["//ul[contains(@class,'sitenav-sub-column')]//li",
                                            "//*[contains(@class,'mz-pagenumbers-next')]"])),
        Rule(LinkExtractor(restrict_xpaths=["//*[contains(@class,'mz-productlist-list mz-l-tiles')]//li"]),
             callback='parse_product_contents'),
    )

    def parse_product_contents(self, response):
        item = BlueflyItem()
        item['brand'] = self.product_brand(response)
        item['category'] = self.product_category(response)
        item['description'] = self.product_description(response)
        item['gender'] = self.product_gender(response)
        item['image_urls'] = self.product_image_urls(response)
        item['market'] = 'US'
        item['merch_info'] = self.product_merch_info(response)
        item['name'] = self.product_name(response)
        item['retailer'] = self.product_retailer(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['skus'] = self.product_sku(response)
        item['url'] = response.url
        item['url_original'] = response.url
        yield item

    def product_brand(self, response):
        return response.xpath("//p[contains(@class,'mz-productbrand')]/a/text()").extract()[0]

    def product_category(self, response):
        return response.xpath("//a[@class='mz-breadcrumb-link']/text()").extract()

    def product_retailer_sku(self, response):
        retailer_sku = response.xpath("//li[@itemprop='productID']//text()").extract()
        return retailer_sku[0].split()[-1]

    def product_description(self, response):
        description = response.xpath("//*[contains(@class,'mz-productdetail-description')]//text()").extract()
        detail = response.xpath("//ul[contains(@class,'mz-productdetail-props')]/li[not(@itemprop)]/text()").extract()
        return description + detail

    def product_image_urls(self, response):
        return response.xpath('//a[contains(@class,"mz-productimages-thumb")]//@data-zoom-image').extract()

    def product_merch_info(self, response):
        merch_info = response.xpath('//div[contains(@class,"mz-price-message")]/text()').extract()
        return [merch_info[0].strip()] if merch_info else ''

    def product_name(self, response):
        name = response.xpath("//*[contains(@class,'mz-breadcrumb-current')]//text()").extract()[0]
        brand = self.product_brand(response)
        return name.replace(brand + " ", '').title()

    def product_retailer(self, response):
        return response.xpath('//a/div[contains(@class,"site-toggler")]//text()').extract()[0].strip()

    def product_gender(self, response):
        gender_list = ['Women', 'Men', 'Kids', 'Girls', ' Boys']
        category = self.product_category(response)
        for gender in category:
            return gender if gender in gender_list else 'unisex-adults'

    def product_sku(self, response):
        skus = {}
        sizes = response.xpath("//*[contains(@class,'mz-productoptions-sizebox')]")
        colour = response.xpath("//span[contains(@class,'mz-productoptions-optionvalue')]//text()").extract()
        prev_price = self.product_prev_price(response)
        price = self.product_price(response)
        if sizes:
            for size in sizes:
                sku = {}
                sku['colour'] = colour
                sku['currency'] = 'USD'
                if prev_price:
                    sku['previous_prices'] = prev_price
                sku['price'] = price
                sku['size'] = size.xpath('.//text()').extract()
                key = size.xpath('@data-value').extract()
                skus[key[0]] = sku
        else:
            sku = {}
            sku['colour'] = colour
            sku['currency'] = 'USD'
            if prev_price:
                sku['previous_prices'] = prev_price
            sku['price'] = price
            sku['size'] = 'One Size'
            key = self.product_retailer_sku(response)
            skus[key] = sku
        return skus

    def product_price(self, response):
        price = response.xpath('//div[@itemprop="price"]//text() | //div[@class="mz-price"]//text()').extract()
        return price[0].strip().split('$', 1)[-1]

    def product_prev_price(self, response):
        prev_price = response.xpath("//*[contains(@class,'mz-price is-crossedout')]//text()").extract()
        return prev_price[-1].strip().split('$', 1)[-1] if prev_price else ''