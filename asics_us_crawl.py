from asics_us.items import AsicsItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class AsicsUSCrawl(CrawlSpider):
    name = 'asics_us_crawl'
    allowed_domains = ['asics.com']
    start_urls = [
        'http://www.asics.com/us/en-us/',
    ]
    rules = [
        Rule(LinkExtractor(restrict_css=['#main-menu']),),
        Rule(LinkExtractor(restrict_css=['#nextPageLink']),),
        Rule(LinkExtractor(restrict_css='.product-list>div>div'), 
            callback='parse_item', follow=True)
    ]
    def parse_item(self, response):
        print(response.url)
        item = AsicsItem()
        item['spider_name'] = 'asics-us-crawl'
        item['retailer'] = 'asics-us'
        item['currency'] = 'USD'
        item['market'] = 'US'
        #item['category'] = response.css('p.prod-classification-reference::text').extract()
        item['retailer_sku'] = response.css('#right-column>p:nth-child(1)>span::text').extract()
        item['price'] = response.css('p.price>span>meta:nth-child(2)::attr(content)').extract()
        item['description'] = response.css('.tabInfoChildContent::text').extract()
        item['url_original'] = response.url
        item['brand'] = 'ASICS'
        item['color'] = response.css('.single-prod-meta.sizes > span::text').extract()
        item['image_urls'] = response.css('.rsNav.rsThumbs.rsThumbsVer > div > img ::attr(src').extract()
        #item['date'] = "Not Set Yet"
        item['skus'] = self.get_sku(response)
        item['care'] = response.css('div.clickTabs > div:nth-child(3) > div.tabInfoChildContent > p:nth-child(2)::text').extract()
        item['name'] = response.css('#right-column > h1::text').extract()
        item['url'] = response.url
        item['gender'] = response.css('li.bv-author-cdv.bv-last > span.bv-author-userinfo-value').extract()
        item['industry'] = 'None'
        #input("enter to next item...")
        yield item

    def get_sku(self, response):
        sku = {}
        sku['currency'] = 'USD'
        sku['color'] = response.css('.single-prod-meta.sizes > span::text').extract()
        sku['out_of_stock'] = 'false'
        sku['price'] = response.css('p.price>span>meta:nth-child(2)::attr(content)').extract()
        #sku['size'] = "Not set yet"
        return sku
