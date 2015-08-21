from scrapy.spiders 		import BaseSpider
from scrapy.selector 		import HtmlXPathSelector
from veromoda_spider.items		import VeromodaSpiderItem
from scrapy.http		import Request
import json

class veromoda_crawler(BaseSpider):
    name = "veromoda"
    allowed_domians = ["veromoda.com"]
    start_urls = ["http://www.veromoda.com/vero-moda/jjumpsuits/vmsassa-flare-2-4-jumpsuit-nfs/10146606,en_GB,pd.html?dwvar_10146606_colorPattern=10146606_Black/"]
	
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        data = hxs.select('//div[@id="breadcrumb"]/div/a/span/text()').extract()
        care_instructions = hxs.select('//div[@class="tabs__half  tabs__half--last"]/div[@class="tabs__content"]/p/text()').extract()
        name = hxs.select('//h1[@class="productname"]/text()').extract()
        description = hxs.select('//div[@class="tabs__half tabs__half--first"]/div[@class="tabs__content"]/p/text()').extract()
        # Not Working
        img_urls =  hxs.select('//li[@class="lslide active" or @class="lslide"]/img/@src').extract()
        url_orignal = response.url
        # skus = hxs.select('//div[@id="jsVariantsJSON"]/comment()')
        brand = hxs.select('//div[@class="productimage js-product-image concealed"]/a/@href')
        product_id = hxs.select('//*[@id="pdpMain"]/div[1]/div[2]/div[1]/a/@href')
		
        for line in data:
            item = VeromodaSpiderItem()
            #item ["product_id"] = product_id
            item["care"] = care_instructions[0]
            item["category"] = line
            item["name"] = name
            item["description"] = description
            item["image_urls"] = img_urls
            item["url_orignal"] = url_orignal
            item["brand"] = int(brand)
            # item["skus"] = skus
            yield item
			
			
			
