import scrapy


class HypedcSpider(scrapy.Spider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = ['http://hypedc.com']

    def parse(self, response):
        # Get the links of all the sections.
        section_url = response.css('a.dropdown-toggle::attr(href)').extract()

        # Remove unwanted sections from the list.
        section_url.remove('#')
        section_url.remove('https://www.hypedc.com/brands/')
        section_url.remove('/checkout/cart')

        for section in section_url:
            yield scrapy.Request(url=section_url[0], callback=self.parse_section)

    def parse_section(self, response):
        # Get the links of all the shoes on current page.
        shoe_url = response.css('div.col-xs-12 > a::attr(href)').extract()

        for shoes in shoe_url:
            yield scrapy.Request(url=shoes, callback=self.parse_shoe)

    def parse_shoe(self, response):
        # Get the details of all the shoes.
        shoe = {
            'name': (response.css('h1.product-name::text').extract_first()).strip(),
            'colour': (response.css('h3.product-colour::text').extract_first()).strip(),
            'price': response.css('h2.product-price::attr(data-bf-productprice)').extract_first(),
            'description': (response.css('div[itemprop="description"]::text').extract_first()).strip(),
            'specification': response.css('div[itemprop="description"] > ul > li').extract(),
        }

        # Get the links to available sizes of current shoe.
        shoe_size = {
            'type_link': response.css('ul[id="size-selector-desktop-tabs"] > li > a::attr(href)').extract(),
            'type_name': response.css('ul[id="size-selector-desktop-tabs"] > li > a::text').extract(),
        }

        # Get the available sizes from the links.
        for x in range(0, len(shoe_size['type_link'])):
            shoe_size['type_link'][x] = shoe_size['type_link'][x][1:]
            shoe['size - ' + shoe_size['type_name'][x]] = response.css('div[id="' + shoe_size['type_link'][x] + '"] > ul.list-inline > li[data-stock="in"] > a::text').extract()

        # Append sizes to shoe dictionary
        shoe['specification'] = [line.replace('<li>', '').replace('</li>', '') for line in shoe['specification']]

        # follow pagination link
        next_page_url = response.css('div.col-xs-4 > a.btn-primary::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_section)

        yield shoe
