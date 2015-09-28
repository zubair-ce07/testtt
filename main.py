__author__ = 'root'
##########################
# Command Line Interface #
##########################
import parallel_crawler
import sys
import stat_summary


def main(args):

    if len(args) < 3:
        print("No arguments have been passed. Exiting System")
        sys.exit()

    elif len(args) >= 3:
        print "Starting the project"
        pc = parallel_crawler.ParallelCrawler(args[0], int(args[1]), int(args[2]))
        pc.make_processes()

        #: Output the calculated results
        statistics_summary = pc.summary
        print '##########################'
        print '#         Output         #'
        print '##########################'
        print statistics_summary.avg_page_size
        print statistics_summary.no_of_requests
        print statistics_summary.total_bytes_downloaded
    return

if __name__ == "__main__":
    main(sys.argv[1:])
