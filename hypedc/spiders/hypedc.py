import scrapy


class HypedcSpider(scrapy.Spider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = ['http://hypedc.com']

    def parse(self, response):
        # Get the links of all wanted the sections.
        section_url = response.css('a[data-toggle="dropdown"]::attr(href)')[1:].extract()

        for section in section_url:
            yield scrapy.Request(url=section, callback=self.parse_section)

    def parse_section(self, response):
        # Get the links of all the shoes on current page.
        shoe_url = response.css('div.item > a::attr(href)').extract()

        for shoe in shoe_url:
            yield scrapy.Request(url=shoe, callback=self.parse_shoe)

        # follow pagination link
        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_section)

    def parse_shoe(self, response):
        # Get the details of all the shoes.
        shoe = {
            'name': response.css('h1.product-name::text').extract_first('').strip(),
            'colour': response.css('h3.product-colour::text').extract_first('').strip(),
            'price': response.css('h2.product-price::attr(data-bf-productprice)').extract_first(''),
            'description': response.css('div[itemprop="description"]::text').extract_first('').strip(),
            'specification': response.css('div[itemprop="description"] > ul > li').extract(),
        }

        # Remove unwanted characters from each specification string.
        shoe['specification'] = [line.replace('<li>', '').replace('</li>', '') for line in shoe['specification']]

        # Get the links to available sizes of current shoe.
        shoe_size = {
            'size_link': response.css('ul[id="size-selector-desktop-tabs"] > li > a::attr(href)').extract(),
            'size_name': response.css('ul[id="size-selector-desktop-tabs"] > li > a::text').extract(),
        }

        for size_no in range(0, len(shoe_size['size_link'])):

            shoe_size['size_link'][size_no] = shoe_size['size_link'][size_no][1:]

            # Get the available sizes from the links
            all_sizes = response.css('div[id="' + shoe_size['size_link'][size_no]
                                     + '"] > ul.list-inline > li[data-stock="in"] > a::text').extract()

            # Append sizes to shoe dictionary.
            shoe['size - ' + shoe_size['size_name'][size_no]] = all_sizes

        yield shoe
