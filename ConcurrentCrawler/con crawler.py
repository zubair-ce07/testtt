from Functions import get_urls
from Classes import ConcurrentCrawler


def main():

    urls = get_urls('http://yahoo.com')
    max_threads = 10
    max_urls = 100
    time_delay = 5

    concurrent_crawler = ConcurrentCrawler(urls, max_threads, max_urls, time_delay)
    concurrent_crawler.event_loop()
    average = concurrent_crawler.length / max_urls
    print('\nTotal Requests made: {}'.format(concurrent_crawler.request_count))
    print('Total Bytes Downloaded: {}'.format(concurrent_crawler.length))
    print('Average File Size: {}'.format(average))


if __name__ == '__main__':

    main()