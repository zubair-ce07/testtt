import argparse

import crawler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Enter the website url')
    parser.add_argument('-d', help='Specify download delay')
    parser.add_argument('-r', help='Specify number of concurrent requests')
    parser.add_argument('-m', help='Specify the maximum number of urls should be visited')
    args = parser.parse_args()
    if args.u:
        if not args.u.endswith('/'):
            args.u += '/'
    else:
        args.u = 'https://www.tutorialspoint.com/'
    if args.r:
        args.r = int(args.r)
    else:
        args.r = 8
    if args.d:
        args.d = float(args.d)
    else:
        args.d = 0.5
    if args.m:
        args.m = int(args.m)
    else:
        args.m = 30
    async_crawler = crawler.AsyncCrawler(args.u, args.r, args.d, args.m)
    async_crawler.start()
    async_crawler.show_performance('Asynchronous')
    parallel_crawler = crawler.ParallelCrawler(args.u, args.r, args.d, args.m)
    parallel_crawler.start()
    parallel_crawler.show_performance('Parallel')
