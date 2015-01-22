from bottegaveneta.items import BottegavenetaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urljoin


def convert_into_absolute_url(value):
    if ('http:/' not in value):
        value = urljoin('http://www.bottegaveneta.com/', value)
    return value

class BottegavenetaSpider(CrawlSpider):
    name = "bottegavenetaSpider"
    allowed_domains = ["bottegaveneta.com"]
    start_urls = [
        "http://www.bottegaveneta.com/us"
    ]
    first_page_xpath = './/*[@id="menuContainer"]//ul[1]//ul//li/a'
    article_page_xpath = './/*[@id="grid_container"]/article[position()<4]/div[@class="overlay"]/a'
    items_page_xpath = './/*[@id="results"]/div[position()<3]/a'
    product_response = ''
    rules = [
        Rule(SgmlLinkExtractor(deny=(r'home_section', r'furniture_section'), restrict_xpaths=first_page_xpath)),
        Rule(SgmlLinkExtractor(deny=(r'home_section', r'furniture_section'), restrict_xpaths=article_page_xpath)),
        #rule which is used to extract links from first page main menu
        Rule(SgmlLinkExtractor(restrict_xpaths=items_page_xpath, deny=[r'home_section']), callback='parse_get_detail'),
        #rule is used to extract product's details

    ]

    def parse_get_detail(self, response):
        self.product_response = response
        item = BottegavenetaItem()
        for res in self.product_response.xpath('.//*[@id="itemInfoBox"]'):
            item['retailer'] = 'bottegaveneta'
            if ('gb' in self.product_response.url):
                item['currency'] = 'Pound'
            else:
                item['currency'] = 'USD'
            item['spider_name'] = self.name
            item['category'] = self.get_category()
            item['url'] = self.product_response.url
            item['title'] = self.get_title(res)
            item['retailer_sk'] = self.get_retailer_sk()
            item['color'] = self.get_color(res)
            item['image_urls'] = self.get_images(res)
            item['description'] = self.get_description(res)
            item['skus'] = self.get_skus(res)
            yield item

    def get_category(self):
        category = self.product_response.xpath('.//*[@id="bread"]/div[@class="breadContainer"]/span[position()>1]//a/text()').extract()
        return category

    def get_title(self, response):
        title = response.xpath('.//*[@class="product-title"]//span/text()').extract()[0]
        return title

    def get_retailer_sk(self):
        retailer_sk = self.product_response.xpath('.//*[@id="itemContent"]/@data-default-code10').extract()[0]
        return retailer_sk

    def get_color(self, response):
        color = response.xpath('.//*[@id="pageColorThumbs"]/li[1]/@title').extract()[0]
        return color

    def get_images(self, response):
        images = []
        for img in response.xpath('.//*[@id="thumbsContainerImg"]/img/@src').extract():
            images.append(img.replace('_11_', '_15_'))
        return images

    def get_description(self, response):
        description = []
        description = response.xpath('.//*[@class="tab1 editorialdescription"]/text()').extract()
        description.append(response.xpath('//*[@class="tab2 details"]/text()').extract())
        for values in response.xpath('//*[@class="tab2 details"]/span[@class="value"]'):
            description.append(values.xpath('./text()').extract())
        return description

    def get_price(self, response):
        price = response.xpath('.//*[@class="price" or @class="itemBoxPrice"]/text()').extract()[0]
        return price

    def get_skus(self, res):
        skus = {}
        for sizes in res.xpath('.//*[@id="sizesUl"]/li'):
            arr = {}
            arr['currency'] = 'USD'
            arr['colour'] = self.get_color(res)
            arr['price'] = self.get_price(res)
            arr['size'] = sizes.xpath('./@title').extract()[0]
            skus[arr['size'] + '_' + arr['colour']] = arr
        return skus

