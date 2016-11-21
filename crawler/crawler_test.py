from ConcurrentCrawler import ConcurrentCrawler
from ParallelCrawler import ParallelCrawler


def main():
    start_url = 'http://quotes.toscrape.com/'
    # Testing Concurrent Crawler
    print('Crawling {} with concurrent crawler...'.format(start_url))
    crawler = ConcurrentCrawler(10, 1.0, 10)  # Follow only 10 links
    crawler.start_crawl(start_url)
    show_results(crawler)

    # Testing Parallel Crawler
    print('Crawling {} with parallel crawler...'.format(start_url))
    crawler = ParallelCrawler(10, 1.0, 10)
    crawler.start_crawl(start_url)
    show_results(crawler)


def show_results(crawler):
    print('URLs visited: ', len(crawler.visited))
    print("Bytes: ", crawler.byte_count)
    print('Average Page Size: ', crawler.byte_count // len(crawler.visited))

if __name__ == '__main__':
    main()
