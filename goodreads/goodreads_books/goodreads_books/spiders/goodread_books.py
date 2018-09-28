# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, Identity, MapCompose

from ..spiders import goodreads


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


class GoodreadBooksSpider(goodreads.GoodReadsAuthorsSpider):
    name = 'goodread_books'

    def parse_author(self, response):
        il = goodreads.GoodReadsItemLoader(selector=response)
        attr_il = goodreads.GoodReadsAttributesItemLoader(selector=response)
        attr_il.add_xpath('born', '//div[contains(text(),"Born")]/following-sibling::text()',
                          lambda x: ''.join(x).strip())
        attr_il.add_xpath('website',
                          '//div[contains(text(),"Website")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('twitter',
                          '//div[contains(text(),"Twitter")]/following-sibling::div[@class="dataItem"]//@href')
        attr_il.add_xpath('genre',
                          '//div[contains(text(),"Genre")]/following-sibling::div[@class="dataItem"][1]//@href',
                          lambda x: [f'https://www.goodreads.com{xx}' for xx in x])
        attr_il.add_xpath('member',
                          '//div[contains(text(),"Member")]/following-sibling::div[@class="dataItem"][1]/text()')
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

        author_item = il.load_item()

        if b'More books by' in response.body:
            books_url = response.url.replace('/show/', '/list/') + '?page=1&per_page=1500'
            yield Request(books_url, callback=self.get_books, meta={"item": author_item})
        else:
            response.meta["item"] = author_item
            yield from self.get_books(response)

    def get_books(self, response):
        book_urls = response.xpath(
            "//tr[@itemtype='http://schema.org/Book']//a[@class='bookTitle']/@href").extract()
        for url in book_urls:
            yield response.follow(url, callback=self.parse_book, meta=response.meta)

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

        goodread_il = goodreads.GoodReadsItemLoader(item=response.meta["item"])
        goodread_il.add_value("books", [il.load_item()])

        yield goodread_il.load_item()
