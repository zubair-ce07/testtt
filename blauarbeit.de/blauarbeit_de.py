import re

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapylab.items import BlauarBeitItemLoader


class BlauarBeit(CrawlSpider):
    name = 'blauarbeit'
    allowed_domains = ['blauarbeit.de']
    start_urls = ['https://www.blauarbeit.de/branchenbuch/handwerker/index.html']

    def parse(self, response):
        cat_urls = response.css('#cat_construc a::attr(href)').extract()
        search_categories = response.css('#cat_construc a::text').extract()

        category_dict = dict(zip(search_categories, cat_urls))

        for search_category, cat_url in category_dict.items():
            request = Request(response.urljoin(cat_url), callback=self.parse_urls)
            request.meta['search_category'] = search_category
            yield request

    def pagination(self, response):
        next_url = response.css('.next::attr(href)').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta.get('search_category')
        return request

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.name a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta.get('search_category')
            yield request

    def parse_item(self, response):
        loader = BlauarBeitItemLoader(response=response)

        loader.add_value('search_category', "handwerker,{}".format(response.meta.get('search_category')))
        loader.add_value('url', response.url)
        loader.add_css('company_name', '.profile_top h2::text')
        loader.add_css('about_us', '#cont_about .overview ::text')
        loader.add_css('certifications', '#cont_certs td ::text')

        xpath = '//tr//td[text()="{0}"]/following::td[1]/{1}'
        loader.add_xpath('telephone', xpath.format("Tel:", "text()"))
        loader.add_xpath('address', xpath.format("Addresse:", "text()"))
        loader.add_xpath('categories', xpath.format("Branche:", "/a//text()"))
        loader.add_xpath('website', xpath.format("Homepage:", "a/@href"))

        raw_postcode = response.xpath(xpath.format("Addresse:", "text()")).extract()
        raw_postcode = " ".join(raw_postcode)
        if raw_postcode:
            post_code = re.findall('\s([\d|\-]{4,})\s', raw_postcode)
            if post_code:
                loader.add_value('postcode', post_code[0]),

        no_of_rev = response.css('#ratings h4 span::text').extract_first()
        loader.add_css('average_rating', '#ratings .rdetail_content::text')
        loader.add_css('review_content', '#cont_ratings .p_text::text')
        loader.add_value('number_of_reviews', no_of_rev)
        loader.add_css('blauarbeit_index', '#qindex .qindex_content::text')

        item = loader.load_item()
        if no_of_rev:
            response.meta['item'] = item
            yield self.parse_reviews(response)

        else:
            yield item

    def parse_reviews(self, response):
        item = response.meta.get('item')
        raw_reviews = response.css('#cont_ratings .p_text::text').extract()
        item['review_content'] = item['review_content'] + raw_reviews

        next_link = self.next_review_link(response)
        if next_link:
            request = Request(response.urljoin(next_link), callback=self.parse_reviews, meta={'item': item})
            return request
        else:
            item['review_content'] = ' | '.join([r.strip() for r in item['review_content'] if len(r.strip())])
            return item

    def _extract_revpage_no(self, response):
        raw_next_url = response.xpath('//a[contains(text(),"Weiter")]/@href').re('JavaScript:nextPage\((.*)\);')
        return raw_next_url[0] if raw_next_url else  ''

    def next_review_link(self, response):
        raw_link = response.xpath('//script[contains(text(),"nextPage(interval)")]').re('location.href = (.*);')
        rev_nxtpage = self._extract_revpage_no(response)
        if rev_nxtpage:
            rev_link = raw_link[0].replace('"+interval+"', rev_nxtpage).replace("\"", "")
            return rev_link
        else:
            return rev_nxtpage
