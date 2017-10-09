import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for link in response.css('.author + a::attr(href)'):
            yield response.follow(link, self.parse_author)

        for link in response.css('li.next a::attr(href)'):
            yield response.follow(link, self.parse)

    def parse_author(self, response):
        yield {
            'Description': response.css('div.author-description::text').extract_first().strip(),
            'DOB': response.css('span.author-born-date::text').extract_first(),
            'Title': response.css('h3.author-title::text').extract_first()
        }
