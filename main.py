import argparse

from concurrent_crawler import ConcurrentCrawler
from parallel_crawler import ParallelCrawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', action='store_true',
                       help="Select concurrent implementation")
    group.add_argument('-p', action='store_true',
                       help="Select parallel implementation")

    parser.add_argument('starting_url', type=str,
                        help="The url you want to recursively crawl")
    parser.add_argument('-w', type=int, default=5,
                        help='Number of workers')
    parser.add_argument('-n', type=int, default=10,
                        help='Maximum URLs to crawl')
    parser.add_argument('-d', type=float, default=1.0,
                        help='Delay between each request (for each worker)')

    args = parser.parse_args()
    if args.c:
        crawler = ConcurrentCrawler(args.w, args.n, args.d)
    elif args.p:
        crawler = ParallelCrawler(args.w, args.n, args.d)

    crawler.crawl(args.starting_url)
