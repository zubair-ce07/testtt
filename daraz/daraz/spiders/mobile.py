import scrapy

class MobileSpider(scrapy.Spider):

    name = 'mobile'
    start_urls = [
                    'https://www.daraz.pk/phones-tablets/samsung/'
                 ]

    def parse(self, response):
        for link in response.css('section.products .link'):
            brand = link.css('.brand::text').extract_first()
            model = link.css('span.name::text').extract_first()
            if model:
                price = link.css('span.price span::text')[1].extract()
                specs = model.split('-')
                ram = next((s for s in specs if 'RAM' in s), None)
                rom = next((s for s in specs if 'ROM' in s), None)
                if ram and rom is None:
                    rom = next((s for s in specs if 'GB' in s and s != ram), None)
                if ram is None and rom is None:
                    ram = next((s for s in specs if 'GB' in s), None)
                    rom = next((s for s in specs if 'GB' in s and s != ram), None)
                    if ram and not rom:
                        rom = ram
                        ram = None
                    try:
                        if ram and rom and float(ram.split('G')[0]) > float(rom.split('G')[0]):
                            ram,rom = rom,ram
                    except ValueError as e:
                        print "Error"
                cam = next((s for s in specs if 'MP' in s), None)
                size = next((s for s in specs if '\"' in s), None)
                yield {
                    'Brand': brand,
                    'Price': price,
                    'Model': specs[0],
                    'Size': size,
                    'Ram': ram,
                    'Rom': rom,
                    'Camera': cam,
                    'Descrip': model
                    }
        next_page = response.css('section.pagination li.-selected + li a::attr(href)').extract_first()
        print "Next Page", next_page
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
