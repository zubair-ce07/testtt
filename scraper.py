import argparse
from parserfactory import ParserFactory
import time

from elements.webpage import WebPage
from elements.hyperlink import HyperLink
from elements.span import Span
from elements.listitem import ListItem
from elements.division import Division
from elements.attribute import Attribute
from elements.text import Text


class Scraper:
    @staticmethod
    def main():
        arg_parser = argparse.ArgumentParser(description='Crawl Web')
        arg_parser.add_argument("type", help="Parser Type")
        arg_parser.add_argument('-d', metavar='N', nargs='+', type=int,
                                help='Download Delay')
        arg_parser.add_argument('-m', metavar='N', nargs='+', type=int,
                                help='Max request count')
        arg_parser.add_argument('-c', metavar='N', nargs='+', type=int,
                                help='Max Concurrent Request')
        arg_list = arg_parser.parse_args()
        download_delay = 0
        max_request = 1000
        concurrent_request_count = 1000
        if arg_list.d is not None:
            download_delay = int(arg_list.d[0])
        if arg_list.m is not None:
            max_request = int(arg_list.m[0])
        if arg_list.c is not None:
            concurrent_request_count = int(arg_list.c[0])

        parser_structure = Scraper.define_html_structure()

        crawler = ParserFactory.get_parser(arg_list.type,
                                           download_delay,
                                           max_request,
                                           concurrent_request_count)

        start = time.time()
        crawler.crawl(parser_structure)
        end = time.time()

        print("Total Time Taken = " + str(end - start))
        print("Total Bytes Downloaded = " + str(crawler.total_bytes_downloaded))
        print("Total Request = " + str(crawler.request_count))
        print("Average Size of a Page = " + str(crawler.total_bytes_downloaded / crawler.request_count))

    @staticmethod
    def define_html_structure():
        web_page = WebPage()
        web_page.url = "https://www.trulia.com/for_rent/New_York,NY"
        root = "//div[@id='resultsColumn']//div[contains(@class, 'containerFluid')]//ul[contains(@class,'mvn')]"
        pagination = Division()
        pagination.css_class = "paginationContainer"
        page = WebPage()
        page.css_class = 'phm'
        page_number = Attribute()
        page_number.attribute_name = "aria-label"
        advert_item = ListItem()
        advert_item.root_path = root
        advert_item.multiple = True
        advert_item.css_class = "xsCol12Landscape"
        advert_item.direct_child = True
        price = Span()
        price_text = Text()
        price_text.name = "price"
        price.add_leaf_element(price_text)
        price.css_class = "cardPrice"
        title = HyperLink()
        title_name = Attribute()
        title_name.attribute_name = "alt"
        title_name.name = "title"
        title.add_leaf_element(title_name)
        title.only_class = "tileLink"
        sub_page = WebPage()
        sub_page.css_class = "tileLink"
        sub_page.url = "https://www.trulia.com"
        property_detail = ListItem()
        property_detail.root_path = "(//div[@id='propertyDetails']/div[contains(@class,'ptm')]/ul)[1]"
        property_detail.multiple = True
        detail = Text()
        detail.name = "detail"

        property_detail.add_leaf_element(detail)
        sub_page.add_data_element(property_detail)
        advert_item.add_crawlable_link(sub_page)
        advert_item.add_data_element(price)
        advert_item.add_data_element(title)
        page.add_leaf_element(page_number)
        page.add_data_element(advert_item)
        pagination.add_crawlable_link(page)
        web_page.add_data_element(pagination)
        web_page.add_data_element(advert_item)
        return web_page


if __name__ == "__main__":
    Scraper.main()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(Scraper.main())
    # loop.close()
