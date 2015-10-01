##########################
# Command Line Interface #
##########################
import parallel_crawler
import argparse
import stat_summary


def main(args):

    pc = parallel_crawler.ParallelCrawler(args.base_url, args.allowed_domain, args.no_of_parallel_requests,
                                          args.download_delay)
    total_bytes, total_requests = pc.make_processes()
    ss = stat_summary.StatSummary(total_requests, total_bytes)

    #: Output the calculated results
    print '##########################'
    print '#         Output         #'
    print '##########################'
    ss.display_summary()
    return

#: Sample input
#: python main.py "http://arbisoft.com" "arbisoft.com" 4 0
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url', nargs='?', action="store", default='http://arbisoft.com/', type=str)
    parser.add_argument('allowed_domain', nargs='?', action="store", default='arbisoft.com', type=str)
    parser.add_argument('no_of_parallel_requests', nargs='?', action="store", default=2, type=int)
    parser.add_argument('download_delay', nargs='?', action="store", default=0, type=int)
    main(parser.parse_args())
