import re
import json
from scrapy.spiders 		import BaseSpider
from scrapy.selector 		import HtmlXPathSelector
from veromoda_spider.items		import VeromodaSpiderItem
from veromoda_spider.items		import skuItem
from scrapy.http		import Request
from scrapy.utils.serialize import ScrapyJSONEncoder

class veromoda_crawler(BaseSpider):
    name = "veromoda"
    allowed_domians = ["veromoda.com"]
    start_urls = ["http://www.veromoda.com/vero-moda/jjumpsuits/vmsassa-flare-2-4-jumpsuit-nfs/10146606,en_GB,pd.html?dwvar_10146606_colorPattern=10146606_Black/"]

    def get_skus(self, skus):
	
        # Make a dictionary
        skus_dictionary={}
		
        # Using regular expressin to remove comments
        skus = re.sub(ur'\s', u'', skus, flags=re.UNICODE)
        skus = re.sub(ur'<!--\[\w*\]>', u'', skus, flags=re.UNICODE)
        skus = re.sub(ur'<!\[\w*\]-->', u'', skus, flags=re.UNICODE)
        # Convert Unicode to string
        [str(x) for x in skus]
        # Convert string to dictionary
        skus = json.loads(skus)
        # Check how many items are there in the dictionary
        length_of_skus = len(skus["10146606"]["variations"]["variants"])
        i = 0
        while (i < length_of_skus):
            item = skuItem()
            item["price"] = skus["10146606"]["variations"]["variants"][i]["pricing"]["standard"]
            item["out_of_stock"] = not(skus["10146606"]["variations"]["variants"][i]["inWarehouse"])
            item["color"] = skus["10146606"]["variations"]["variants"][i]["attributes"]["colorPattern"]
            item["size"] = skus["10146606"]["variations"]["variants"][i]["attributes"]["size"]
            key = skus["10146606"]["variations"]["variants"][i]["id"]
            skus_dictionary[key] = item 
            i = i + 1

        return skus_dictionary
		
    def get_name(self, name):
	
        # Remove white space characters
        name = re.sub(ur'\s', u'', name, flags=re.UNICODE)
        return name
		
    def parse(self, response):
	
        hxs = HtmlXPathSelector(response)
		
        # Extracting data grom the page 
        category = hxs.select('//div[@id="breadcrumb"]/div/a/span/text()').extract()
        care_instructions = hxs.select('//div[@class="tabs__half  tabs__half--last"]/div[@class="tabs__content"]/p/text()').extract()
        name = self.get_name(hxs.select('//h1[@class="productname"]/text()').extract()[0])
        description = hxs.select('//div[@class="tabs__half tabs__half--first"]/div[@class="tabs__content"]/p/text()').extract()
        # Not Working
        img_urls =  hxs.select('//*[@id="pdpMain"]/script[2]/text()').extract()
        url_orignal = response.url
        skus =  self.get_skus(hxs.select('//div[@id="jsVariantsJSON"]/comment()').extract()[0])
        brand = hxs.select('//*[@id="jsCurrentBrand"]/text()').extract()
        product_id = hxs.select('//*[@id="pdpMain"]/div[1]/div[2]/div[1]/a/@href').extract()
		
		
        
        item = VeromodaSpiderItem()
        item ["product_id"] = product_id
        item["care"] = care_instructions[0]
        item["category"] = category
        item["name"] = name
        item["description"] = description
        item["image_urls"] = img_urls
        item["url_orignal"] = url_orignal
        item["brand"] = brand
        item["skus"] = skus
        yield item
			
			

