from Function import get_urls
from ParallelCrawrler import ParallelCrawler

def main():

    urls = get_urls('http://olx.com.pk')
    max_threads = 10
    max_urls = 100
    time_delay = 0.1

   # print(len(urls))
    crawler = ParallelCrawler(urls, max_threads, max_urls, time_delay)
    crawler.start()

    print("\nTotal Requests Made: {0} Requests".format(crawler.request_count))
    print("Total Bytes Downloaded: {0} Bytes".format(crawler.length))
    print("Average Size Of A Page: {0} Bytes".format(round(crawler.length/crawler.request_count,2)))


if __name__ == '__main__':
    main()

