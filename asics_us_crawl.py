from asics_us.items import AsicsItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class AsicsUSCrawl(CrawlSpider):
    name = 'asics_us_crawl'
    start_urls = ["http://www.asics.com/us/en-us/"]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(".//*[@id='main-menu']//ul"
        	"[contains(@class,'childLeafNode')]//li[contains(@class,"
        	"'yCmsComponent')]", ".//*[contains(@class,'nm center')]", ))),
        Rule(LinkExtractor(restrict_xpaths=(".//*[contains(@class,"
        	"'product-list')]/div/div", )), callback='parse_item'),
    )
    def parse_item(self, response):
        article = AsicsItem()
        article['spider_name'] = 'asics-us-crawl'
        article['retailer'] = 'asics-us'
        article['currency'] = 'USD'
        article['market'] = 'US'
        article['price'] = response.xpath(".//*[contains(@class,"
        	"'price')]/span//text()").extract()[-1].strip()
        article['category'] = response.xpath("//*[contains(@id, "
        	"'breadcrumb')]/ul/li[not (@class='active')]/a[not"
        	"(@href='/us/en-us/')]/span/text()").extract()
        description = response.xpath(".//*[contains(@class,"
        	"'tabInfoChildContent')]/text()").extract()
        [x.strip for x in description]
        article['description'] = description
        article['url_original'] = response.url
        article['brand'] = response.xpath(".//*[contains(@class,'singleProduct')]/meta[1]/@content").extract()[-1]
        # article['img_urls'] = self.image_urls(response)
        article['sku'] = self.get_sku(response)
        article['name'] = response.xpath(".//*[contains(@class,'single-prod-title')]/text()").extract()[-1]
        article['url'] = response.url
        article['gender'] = article['category'][0]
        yield article

    def get_sku(self, response):
        sku = {}
        selector = response.xpath(".//*[contains(@id, 'SelectSizeDropDown')]/li[@class='SizeOption inStock']")
        for item in selector:
            sku_details = {}
            sku_details['currency'] = item.xpath("meta[3]/@content").extract()
            sku_details['price'] = item.xpath("meta[4]/@content").extract()[0]
            sku_details['size'] = item.xpath("a/text()").extract()[0].split()
            sku_details['color'] = response.xpath(".//*[contains(@class,'border')]/text()").extract()[0].strip()
            sku_details['previous price'] = response.xpath(".//*[contains(@class,'markdown')]/del/text()").extract()
            sku_details['out_of_stock'] = 'false'
            sku[item.xpath("meta[1]/@content").extract()[0]] = sku_details
        return sku

        '''
    def image_urls(self, response):
        selector = response.xpath(".//*[contains(@id,'product-image-0')]")
        url1 = selector.xpath("./@data-big").extract()[0]
        url2 = selector.xpath("./@data-rstmb").extract()[0]
        src = selector.xpath("./@src").extract()[0]
        return [url1, url2, src]
        return [url2, src]
		'''