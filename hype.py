import scrapy

urls = []


class HypeDC(scrapy.Spider):
    name = "hypedc"
    start_urls = [
        'https://www.hypedc.com/',
    ]

    def parse(self, response):
        urls.append(response.css('a[href$="com/mens/"]::attr(href)').extract_first())
        urls.append(response.css('a[href$="com/womens/"]::attr(href)').extract_first())
        urls.append(response.css('a[href$="com/kids/"]::attr(href)').extract_first())
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        for product_url in response.css('div.item > a::attr(href)').extract():
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        print(response.url)
        yield {
            'Brand': response.css('h2.product-manufacturer::text').extract_first(),
            'Name': response.css('h1.product-name::text').extract_first(),
            'Color': (response.css('h3.product-colour::text').extract_first()).strip(),
            'Price': response.css('div.price-div meta::attr(content)').extract_first(),
            'Description': response.css('div.product-description::text').extract_first().strip(),
            'Breadcrumb': response.css('ul.breadcrumb li a span::text').extract(),
            'Img-Src': response.css('div.slider-inner div.unveil-container noscript img::attr(src)').extract_first(),
            'URL': response.url,
            'Available Sizes': response.css('div#size-selector-tab-desktop-0 > ul li:not(.inactive) a::text').extract(),
        }
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_product)