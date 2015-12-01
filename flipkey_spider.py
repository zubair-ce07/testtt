from scrapy.spiders import Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest, Request
from rent_websites.spiders.RentBaseSpider import RentBaseSpider
from rent_websites.items import PlaceItem
import json
import re


class FlipkeySpider(RentBaseSpider):
    name = "flipkey"
    allowed_domains = ["flipkey.com"]
    start_urls = ['https://www.flipkey.com/vacation-rentals/']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=("//*[@id='popular-destinations']//h5/a",
                                                ))),
        Rule(SgmlLinkExtractor(restrict_xpaths=(
            "//*[@id='region-list']//*[@class='child-region']",)),
            callback="parse_pages", follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=(
            "//*[@data-link-name='title']",)),
            callback="parse_product"),
    )

    def parse_pages(self, response):
        """Handling pagination through POST requests"""

        # extracting request data from page source
        extracted_text = response.xpath('//script[contains(.,"Object.PHPJSON")]//text()').extract()
        json_extracted = re.search("Object.PHPJSON\s*=\s*'([^']+)'", extracted_text[0])

        if json_extracted:
            result = json_extracted.group(1)

        if response.xpath("//*[@class='search-pagination']"):
            # extracting number of result pages for each location
            total_pages_text = response.xpath("(//*[@id='search-pages']/text())").extract()[0]
            total_num_pages = re.search("of\s*(\d+)", total_pages_text)

            if total_num_pages:
                total_num_pages = total_num_pages.group(1)
                for page_number in range(2, int(total_num_pages) + 1):
                    raw_json = json.loads(result)
                    raw_json['page'] = page_number  # substituting required page number in request data
                    result = json.dumps(raw_json)

                    yield FormRequest(url='https://www.flipkey.com/search/filter/?page=' + str(page_number),
                                      formdata={'data': result, "excluded": ""})

    def parse_product(self, response):
        """Function extracting values from product page"""

        item = PlaceItem()
        item['item_source'] = response.url
        item['name'] = self.get_name(response)
        item['price'] = self.get_price(response)
        yield item

    def get_name(self, response):
        return response.xpath("//*[@id='pdp-title']/h1/text()").extract()

    def get_price(self, response):
        price = response.xpath("//*[@id='price_field']/text()").extract()
        return response.xpath("//*[@id='rental_price']/text()").extract()[0].strip() if not price else price
