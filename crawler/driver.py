import  requests
from parsel import  Selector
import concurrent_crawler
import parallelcrawler
import sys

class Extacturls:

    def __init__(self, url):
        self.baseurl = url
        self.urls = self.__extract_urls()
        self.no_of_urls = len(self.urls)

    def __extract_urls(self):
        try:
            html_text = requests.get(self.baseurl).text
            selector = Selector(text=html_text)
            urls = selector.xpath('//a/@href').extract()
            urllist = []
            for url in urls:
                if 'http' not in url:
                    urllist.append(self.baseurl + url)
                else:
                    urllist.append(url)
            return urllist
        except Exception as ex:
            print("Exception occured: ",ex)


def main():
    baseurl = "https://en.wikipedia.org"
    driver = Extacturls(baseurl)
    print(" max urls to visit : {}".format(driver.no_of_urls))
    while True:
        try:
            no_of_requets = int (input(" Specify no of concurrent request : "))
        except ValueError:
            print ("only integer less than {}".format(driver.no_of_urls))
            continue
        if no_of_requets > driver.no_of_urls:
            print("only integer less than {}".format(driver.no_of_urls))
            continue
        else:
            break

    while True:
        try:
            download_delay = int (input(" Download delay  : "))
        except ValueError:
            print ("only integer ")
            continue
        else:
            break

    c_crawl = concurrent_crawler.Asnyccrawler(driver.urls, no_of_requets, download_delay)
    c_crawl.eventloop()

    p_crawl = parallelcrawler.Parallelcrawler(driver.urls , no_of_requets , download_delay)
    p_crawl.run()

    download_size = c_crawl.download_size + p_crawl.download_size + sys.getsizeof(driver.urls)
    print(" report ")
    print(" Bytes Downloaded : {}".format(download_size))
    print(" avg page size : {}".format(c_crawl.avg_page_size))
    print(" total no of requets made: {}".format(min(driver.no_of_urls,no_of_requets)*2))

if __name__ == "__main__":
    main()