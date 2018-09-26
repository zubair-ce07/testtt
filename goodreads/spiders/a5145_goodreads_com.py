import re
from scrapinghub import ScrapinghubClient

from scrapy import Spider, Item, Field, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, MapCompose
from scrapy.shell import inspect_response

from xml.dom import minidom


class GoodReadsAttributesItem(Item):
    born = Field()
    website = Field()
    twitter = Field()
    genre = Field()
    member = Field()
    url = Field()


class GoodReadsBooksItem(Item):
    title = Field()
    gr_url = Field()
    gr_bid = Field()
    author = Field()
    avg_rating = Field()
    rating_count = Field()
    reviews = Field()
    originally_published = Field()
    isbn = Field()
    ean = Field()
    series = Field()
    character = Field()
    setting = Field()
    awards = Field()
    similiar_titles = Field()
    published = Field()
    editions_count = Field()
    gr_edition_url = Field()


class GoodReadsItem(Item):
    gr_aid = Field()
    gr_url = Field()
    name = Field()
    image_url = Field()
    avg_ratings = Field()
    ratings_count = Field()
    reviews = Field()
    distinct_works = Field()
    similar_authors = Field()
    attributes = Field()
    books = Field()


class GoodReadsItemLoader(ItemLoader):
    default_item_class = GoodReadsItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    similar_authors_out = Identity()
    books_out = Identity()


class GoodReadsAttributesItemLoader(ItemLoader):
    default_item_class = GoodReadsAttributesItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    genre_out = Identity()


def _clean_in(loader, values):
    return [x.strip() for x in values]


def _make_isbn(loader, values):
    return [x[3:] for x in values]


def _published_date(loader, value):
    publish_date = re.findall("\\n\s+(.+)\\n", value[0])
    if publish_date:
        return publish_date[0]


class GoodReadsBooksItemLoader(ItemLoader):
    default_item_class = GoodReadsBooksItem

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    title_in = _clean_in
    rating_count_in = _clean_in
    reviews_in = _clean_in
    originally_published_in = _clean_in
    isbn_in = _make_isbn
    gr_edition_url_in = MapCompose(lambda url: "https://www.goodreads.com{}".format(url))

    author_out = Identity()
    series_out = Identity()
    character_out = Identity()
    setting_out = Identity()
    awards_out = Identity()
    similiar_titles_out = Identity()
    originally_published_out = _published_date


class GoodReadsProducerSpider(Spider):
    name = '5145_goodreads_com_producer'

    # There are more than 500 sitemaps available.
    # Parsing only sitemaps with authors
    start_urls = [
        'https://www.goodreads.com/sitemap.162.xml.gz', 'https://www.goodreads.com/sitemap.109.xml.gz',
        'https://www.goodreads.com/sitemap.99.xml.gz', 'https://www.goodreads.com/sitemap.123.xml.gz',
        'https://www.goodreads.com/sitemap.93.xml.gz', 'https://www.goodreads.com/sitemap.163.xml.gz',
        'https://www.goodreads.com/sitemap.116.xml.gz', 'https://www.goodreads.com/sitemap.100.xml.gz',
        'https://www.goodreads.com/sitemap.96.xml.gz', 'https://www.goodreads.com/sitemap.164.xml.gz',
        'https://www.goodreads.com/sitemap.153.xml.gz', 'https://www.goodreads.com/sitemap.97.xml.gz',
        'https://www.goodreads.com/sitemap.95.xml.gz', 'https://www.goodreads.com/sitemap.147.xml.gz',
        'https://www.goodreads.com/sitemap.110.xml.gz', 'https://www.goodreads.com/sitemap.128.xml.gz',
        'https://www.goodreads.com/sitemap.107.xml.gz', 'https://www.goodreads.com/sitemap.92.xml.gz',
        'https://www.goodreads.com/sitemap.145.xml.gz', 'https://www.goodreads.com/sitemap.127.xml.gz',
        'https://www.goodreads.com/sitemap.86.xml.gz', 'https://www.goodreads.com/sitemap.84.xml.gz',
        'https://www.goodreads.com/sitemap.142.xml.gz', 'https://www.goodreads.com/sitemap.156.xml.gz',
        'https://www.goodreads.com/sitemap.130.xml.gz', 'https://www.goodreads.com/sitemap.152.xml.gz',
        'https://www.goodreads.com/sitemap.134.xml.gz', 'https://www.goodreads.com/sitemap.80.xml.gz',
        'https://www.goodreads.com/sitemap.143.xml.gz', 'https://www.goodreads.com/sitemap.78.xml.gz',
        'https://www.goodreads.com/sitemap.161.xml.gz', 'https://www.goodreads.com/sitemap.88.xml.gz',
        'https://www.goodreads.com/sitemap.154.xml.gz', 'https://www.goodreads.com/sitemap.119.xml.gz',
        'https://www.goodreads.com/sitemap.148.xml.gz', 'https://www.goodreads.com/sitemap.94.xml.gz',
        'https://www.goodreads.com/sitemap.125.xml.gz', 'https://www.goodreads.com/sitemap.129.xml.gz',
        'https://www.goodreads.com/sitemap.139.xml.gz', 'https://www.goodreads.com/sitemap.112.xml.gz',
        'https://www.goodreads.com/sitemap.81.xml.gz', 'https://www.goodreads.com/sitemap.121.xml.gz',
        'https://www.goodreads.com/sitemap.118.xml.gz', 'https://www.goodreads.com/sitemap.102.xml.gz',
        'https://www.goodreads.com/sitemap.136.xml.gz', 'https://www.goodreads.com/sitemap.140.xml.gz',
        'https://www.goodreads.com/sitemap.144.xml.gz', 'https://www.goodreads.com/sitemap.106.xml.gz',
        'https://www.goodreads.com/sitemap.160.xml.gz', 'https://www.goodreads.com/sitemap.137.xml.gz',
        'https://www.goodreads.com/sitemap.103.xml.gz', 'https://www.goodreads.com/sitemap.89.xml.gz',
        'https://www.goodreads.com/sitemap.77.xml.gz', 'https://www.goodreads.com/sitemap.117.xml.gz',
        'https://www.goodreads.com/sitemap.124.xml.gz', 'https://www.goodreads.com/sitemap.98.xml.gz',
        'https://www.goodreads.com/sitemap.87.xml.gz', 'https://www.goodreads.com/sitemap.104.xml.gz',
        'https://www.goodreads.com/sitemap.133.xml.gz', 'https://www.goodreads.com/sitemap.85.xml.gz',
        'https://www.goodreads.com/sitemap.111.xml.gz', 'https://www.goodreads.com/sitemap.157.xml.gz',
        'https://www.goodreads.com/sitemap.146.xml.gz', 'https://www.goodreads.com/sitemap.90.xml.gz',
        'https://www.goodreads.com/sitemap.82.xml.gz', 'https://www.goodreads.com/sitemap.149.xml.gz',
        'https://www.goodreads.com/sitemap.159.xml.gz', 'https://www.goodreads.com/sitemap.131.xml.gz',
        'https://www.goodreads.com/sitemap.108.xml.gz', 'https://www.goodreads.com/sitemap.122.xml.gz',
        'https://www.goodreads.com/sitemap.151.xml.gz', 'https://www.goodreads.com/sitemap.126.xml.gz',
        'https://www.goodreads.com/sitemap.132.xml.gz', 'https://www.goodreads.com/sitemap.158.xml.gz',
        'https://www.goodreads.com/sitemap.101.xml.gz', 'https://www.goodreads.com/sitemap.91.xml.gz',
        'https://www.goodreads.com/sitemap.141.xml.gz', 'https://www.goodreads.com/sitemap.138.xml.gz',
        'https://www.goodreads.com/sitemap.120.xml.gz', 'https://www.goodreads.com/sitemap.113.xml.gz',
        'https://www.goodreads.com/sitemap.115.xml.gz', 'https://www.goodreads.com/sitemap.83.xml.gz',
        'https://www.goodreads.com/sitemap.155.xml.gz', 'https://www.goodreads.com/sitemap.105.xml.gz',
        'https://www.goodreads.com/sitemap.114.xml.gz', 'https://www.goodreads.com/sitemap.150.xml.gz',
        'https://www.goodreads.com/sitemap.79.xml.gz', 'https://www.goodreads.com/sitemap.135.xml.gz'
    ]

    def parse(self, response):
        xml_urls = minidom.parseString(response.body)
        xml_urls_list = xml_urls.getElementsByTagName('url')
        for url_object in xml_urls_list:
            url = url_object.getElementsByTagName('loc')[0].firstChild.nodeValue
            if '/author/show' in url:
                yield {'url': url}


class GoodReadsAuthorsSpider(Spider):
    name = '5145_goodreads_com'

    start_urls = ['https://www.goodreads.com/author/on_goodreads']

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        if not hasattr(self, 'job_id'):
            self.log('Input job with author urls missing. Collecting authors from '
                     'https://www.goodreads.com/author/on_goodreads')
            yield Request(self.start_urls[0])
        else:
            client = ScrapinghubClient(self.settings.get('SC_APIKEY'))
            self.job = client.get_job(self.job_id)
            if not hasattr(self, 'start_ind'):
                self.start_ind = 0
            if not hasattr(self, 'end_ind'):
                self.end_ind = 5000000
            for ind, item in enumerate(self.job.items.iter()):
                if int(self.start_ind) <= ind <= int(self.end_ind):
                    yield Request(item.get('url'), callback=self.parse_author,
                                  headers={'Referer': 'https://www.goodreads.com/author/on_goodreads'})

    def parse(self, response):
        if 'goodreads.com' in response.url:
            for url in response.xpath('//a[contains(@href,"/author/show/")]/@href').extract():
                yield response.follow(url, callback=self.parse_author)
            for next_page in response.xpath('//a[@rel="next"]/@href').extract():
                yield response.follow(next_page)

    def parse_author(self, response):
        il = GoodReadsItemLoader(selector=response)
        attr_il = GoodReadsAttributesItemLoader(selector=response)
        attr_il.add_xpath('born', '//div[contains(text(),"Born")]/following-sibling::text()',
                          lambda x: ''.join(x).strip())
        attr_il.add_xpath('website', '//div[contains(text(),"Website")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('twitter', '//div[contains(text(),"Twitter")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('genre', '//div[contains(text(),"Genre")]/following-sibling::div[@class="dataItem"][1]//@href',
                          lambda x: [f'https://www.goodreads.com{xx}' for xx in x])
        attr_il.add_xpath('member', '//div[contains(text(),"Member")]/following-sibling::div[@class="dataItem"][1]/text()')
        attr_il.add_xpath('url', '//div[contains(text(),"URL")]/following-sibling::div[1]/text()',
                          lambda x: ''.join(x).strip())
        attr_item = dict(attr_il.load_item())

        il.add_value('gr_url', response.url)
        il.add_value('gr_aid', response.url, re='/show/(\d+)')
        il.add_value('attributes', attr_item)
        il.add_xpath('name', '//span[@itemprop="name"]/text()')
        il.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        il.add_xpath('avg_ratings', '//div[@class="hreview-aggregate"]//span[@class="average"]/text()')
        il.add_xpath('ratings_count', '//div[@class="hreview-aggregate"]//span[@itemprop="ratingCount"]/@content')
        il.add_xpath('reviews', '//div[@class="hreview-aggregate"]//span[@itemprop="reviewCount"]/@content')
        il.add_xpath('distinct_works', '//a[contains(text(),"distinct work")]/text()', re='\d+')

        #if b'Similar authors' in response.body:
        #    similar_authors_url = response.url.replace('/show/', '/similar/')
        #    r = yield Request(similar_authors_url)
        #    similar_authors = self.get_similar_authors(r)
        #    il.add_value('similar_authors', similar_authors)
        #else:
        #    il.add_value('similar_authors', [])


        author_item = il.load_item()

        if b'More books by' in response.body:
            books_url = response.url.replace('/show/', '/list/') + '?page=1&per_page=1500'
            yield Request(books_url, callback=self.get_books, meta={"item": author_item})
            #books = self.get_books(r)
        else:
            #books = self.get_books(response)
            response.meta["item"] = author_item
            yield from self.get_books(response)


    def get_similar_authors(self, response):
        similar_authors = []
        for author in response.xpath('//li[@class="listElement"]'):
            similar_authors.append({
                'gr_aid': author.xpath('.//a[@class="bookTitle"]/@href').re('/show/(\d+)')[0],
                'gr_url': 'https://www.goodreads.com{}'.format(author.xpath('.//a[@class="bookTitle"]/@href').extract()[0]),
                'author_name': author.xpath('.//a[@class="bookTitle"]/text()').extract()[0]
            })
        return similar_authors[1:]

    def get_books(self, response):
        book_urls = response.xpath("//tr[@itemtype='http://schema.org/Book']//a[@class='bookTitle']/@href").extract()
        for url in book_urls:
            yield response.follow(url, callback=self.parse_book, meta = response.meta)

    def parse_book(self, response):
        goodread_url = "https://www.goodreads.com{}"

        il = GoodReadsBooksItemLoader(response=response)
        il.add_xpath("title", "//*[@id='bookTitle']/text()")
        il.add_value("gr_url", response.url)
        il.add_xpath("gr_bid", "//*[@id='book_id']/@value")
        authors_selectors = response.xpath("//a[@class='authorName']")
        authors = []

        for authors_selector in authors_selectors:
            author = {
                "name": authors_selector.xpath("descendant-or-self::span/text()").extract_first(),
                "url": authors_selector.xpath("@href").extract_first(),
                "gr_aid": authors_selector.xpath("@href").re_first("/(\d+)")
            }
            authors.append(author)

        il.add_value("author", authors)
        il.add_xpath("avg_rating", "//*[@class='average' and @itemprop='ratingValue']/text()")
        il.add_xpath("rating_count", "//meta[@itemprop='ratingCount']/following-sibling::span/text()")
        il.add_xpath("reviews", "//a[@class='gr-hyperlink']//span[contains(@class, 'count')]/text()")
        il.add_xpath("originally_published", "//*[@id='details']/div[2]/text()")
        il.add_xpath("editions_count", "//*[@class='otherEditionsLink']/a/text()")
        il.add_xpath("gr_edition_url", "//*[@class='otherEditionsLink']/a/@href")
        il.add_xpath("isbn", "//span[@itemprop='isbn']/text()")
        il.add_xpath("ean", "//span[@itemprop='isbn']/text()")

        series_selectors = response.xpath("//div[@id='bookDataBox']//*[contains(text(), 'Series')]"
                                          "/following-sibling::div[1]//a[not(@class)]")
        series = []
        for series_selector in series_selectors:
            serie = {
                "name": series_selector.xpath("text()").extract_first(),
                "url": goodread_url.format(series_selector.xpath("@href").extract_first()),
                "gr_series_id": series_selector.xpath("@href").re_first("/(\d+)")
            }
            series.append(serie)

        il.add_value("series", series)

        character_selectors = response.xpath("//div[@id='bookDataBox']//*[contains(text(), 'Characters')]"
                                             "/following-sibling::div[1]//a[not(@class)]")
        characters = []
        for character_selector in character_selectors:
            character = {
                "name": character_selector.xpath("text()").extract_first(),
                "url": goodread_url.format(character_selector.xpath("@href").extract_first()),
                "gr_character_id": character_selector.xpath("@href").re_first("/(\d+)")
            }
            characters.append(character)

        il.add_value("character", characters)

        setting_selectors = response.xpath("//div[@id='bookDataBox']//*[contains(text(), 'setting')]"
                                           "/following-sibling::div[1]//a[not(@class)]")
        settings = []
        for setting_selector in setting_selectors:
            setting = {
                "name": setting_selector.xpath("text()").extract_first(),
                "url": goodread_url.format(setting_selector.xpath("@href").extract_first()),
                "gr_setting_id": setting_selector.xpath("@href").re_first("/(\d+)")
            }
            settings.append(setting)

        il.add_value("setting", settings)

        award_selectors = response.xpath("//*[@itemprop='awards']//a[@class='award']")

        awards = []
        for award_selector in award_selectors:
            award = {
                "name": award_selector.xpath("text()").extract_first(),
                "url": goodread_url.format(award_selector.xpath("@href").extract_first()),
                "gr_setting_id": award_selector.xpath("@href").re_first("/(\d+)")
            }

            awards.append(award)
        il.add_value("awards", awards)

        similar_selectors = response.xpath("//*[contains(@id, 'relatedWorks')]//li//a")

        similars = []
        for similar_selector in similar_selectors:
            similar = {
                "book-title": similar_selector.xpath("descendant-or-self::img/@alt").extract_first(),
                "book_url": similar_selector.xpath("@href").extract_first(),
                "gr_bid": similar_selector.xpath("@href").re_first("/(\d+)")
            }
            similars.append(similar)

        il.add_value("similiar_titles", similars)

        goodread_il = GoodReadsItemLoader(item=response.meta["item"])
        goodread_il.add_value("books", [il.load_item()])

        yield goodread_il.load_item()

    def get_books_old(self, response):
        inspect_response(response, self)
        books = []
        for book in response.xpath('//tr[@itemtype="http://schema.org/Book"]'):
            bil = GoodReadsBooksItemLoader(selector=book)
            bil.add_xpath('title', './/span[@itemprop="name"]/text()')
            bil.add_xpath('gr_url', './/a[@itemprop="url"]/@href',
                          lambda x: f"https://www.goodreads.com{x[0]}" if x else None)
            bil.add_xpath('gr_bid', './/a[@itemprop="url"]/@href',
                          re='/book/show/(\d+)')
            bil.add_xpath('avg_rating', './/span[@class="minirating"]/text()',
                          lambda x: ''.join(re.findall('(.*) avg rating', ''.join(x))).strip())
            bil.add_xpath('rating_count', './/span[@class="minirating"]/text()',
                          lambda x: ''.join(re.findall('— (.*) rating', ''.join(x))).replace(',', '').strip())
            bil.add_xpath('published', './/span[@class="minirating"]/following-sibling::text()',
                          re='\d{4}')
            bil.add_xpath('editions_count', './/span[@class="minirating"]/following-sibling::a/text()',
                          re='(\d+) editions')
            bil.add_xpath('gr_edition_url', './/span[@class="minirating"]/following-sibling::a/@href',
                          lambda x: f"https://www.goodreads.com{''.join(x)}" if x else None)
            b = dict(bil.load_item())
            books.append(b)
        il = GoodReadsItemLoader(item=response.meta["item"])
        il.add_value("books", books)

        yield il.load_item()
